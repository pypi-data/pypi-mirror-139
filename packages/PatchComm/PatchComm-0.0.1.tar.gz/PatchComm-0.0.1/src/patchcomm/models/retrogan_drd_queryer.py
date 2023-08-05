from typing import Dict, List, Union
import os
import numpy as np
# import pandas as pd
import logging
import tensorflow as tf
import torch
import fasttext
import faiss
from rcgan_pytorch import RetroCycleGAN
# from deep_relationship_discovery import load_model_ours


tf.get_logger().setLevel(logging.ERROR)

gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
if gpus:
    try:
        ## Memory growth must be the same across all GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(device=gpu, enable=True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    except RuntimeError:
        ## Memory growth must be set before GPUs are initialized
        print(RuntimeError)


class ConstMultiplierLayer(tf.keras.layers.Layer):
    """
    Customized layer that Pedro had added to DRD -- as far as I know
    - YDX@20210308
    """
    def __init__(self, **kwargs):
        super(ConstMultiplierLayer, self).__init__(**kwargs)
        self.k = self.add_weight(
            name='k',
            shape=(),
            dtype=tf.float32,
            initializer='zeros',
            trainable=True
        )

    def build(self, input_shape):
        super(ConstMultiplierLayer, self).build(input_shape=input_shape)

    def call(self, inputs, **kwargs):
        return tf.multiply(self.k, inputs)

    def compute_output_shape(self, input_shape):
        return input_shape


class RetroganDrdQueryer:
    def __init__(self):
        ## These are attractrepelled Numberbatch embeddings
        ## (i.e., Numberbatch is already retrofitted, and we further retrofit it via AttractRepel)
        self.attractrepelled_numberbatch: Dict[str, np.ndarray] = {}
        with open('src/patchcomm/data/retrogan_data/numberbatch_attractrepel_gold_embeddings.txt', 'r') as f:
            for x in f.readlines():
                x = x.strip().split(' ')
                self.attractrepelled_numberbatch[x[0]] = np.array([np.float32(s) for s in x[1:]], dtype=np.float32)
        self.attractrepelled_numberbatch_words: List[str] = list(self.attractrepelled_numberbatch.keys())
        self.attractrepelled_numberbatch_embeddings: np.ndarray = np.array(
            list(self.attractrepelled_numberbatch.values()),
            dtype=np.float32
        )  # shape == (61914, 300)
        ## FastText model
        self.fasttext_model = fasttext.load_model(
            path='src/patchcomm/models/retrogan_drd_models/fasttext_models/cc.en.300.bin'
        )
        ## RetroGAN model (PyTorch)
        self.retrogan_model = RetroCycleGAN.load_model(
            path='src/patchcomm/models/retrogan_drd_models/retrogan_models/postspec_numberbatch/testcomplete.bin',
            device='cpu'
        )
        ## DRD models (TensorFlow)
        # FIXME
        #   I think that, eventually, I should use Pedro's load_model_ours. But for now, I'll simply use
        #   TensorFlow's built-in load_model, for simplicity.
        # self.drd_models: Dict[str, tf.keras.models.Model] = load_model_ours(
        #     save_folder='patchcomm/models/retrogan_drd_models/drd_models/new'
        # )
        # FIXME
        #   For now, load only the relations that are present in the original OMCS
        with open('src/patchcomm/data/conceptnet_data/conceptnet-assertions-openmindcommonsense-english.txt', 'r') as f:
            omcs_assertions = f.readlines()
        omcs_relations: List[str] = []
        for x in omcs_assertions:
            relation = x.split('\t')[1][3:]
            if relation not in omcs_relations:
                omcs_relations.append(relation)
        self.drd_models: Dict[str, tf.keras.models.Model] = {}
        for x in sorted(os.listdir(path='src/patchcomm/models/retrogan_drd_models/drd_models/new/')):
            if x.endswith('.model'):
                relation = x.replace('.model', '')
                if relation in omcs_relations:
                    self.drd_models[relation] = tf.keras.models.load_model(
                        filepath=f'src/patchcomm/models/retrogan_drd_models/drd_models/new/{x}',
                        custom_objects={'ConstMultiplierLayer': ConstMultiplierLayer},
                        compile=False
                    )

    def getWordEmbedding(self, word: str) -> np.ndarray:
        """
        Generate the post-specialized embedding of the given word.
        """
        ## Generate original FastText embedding via self.fasttext_model
        word_embedding: torch.Tensor = torch.tensor(
            data=self.fasttext_model.get_word_vector(word=word),
            dtype=torch.float32
        )
        ## Generate post-specialized embedding via self.retrogan_model
        word_embedding: torch.Tensor = self.retrogan_model(word_embedding)
        ## Convert the generated PyTorch tensor to TensorFlow tensor
        word_embedding: np.ndarray = word_embedding.detach().numpy().reshape(1, 300)
        return word_embedding

    def getNearestNeighborsForWord(self, word: str, nearest_k=5) -> Dict[str, np.ndarray]:
        """
        For a given word, find its k-nearest neighbors within self.attractrepelled_numberbatch.
        (!!! Note that this is NOT the same as k-Nearest Neighbor algoritm !!!)
        (This is just a similarity search.)
        """
        word_embedding: np.ndarray = self.getWordEmbedding(word=word)
        neighborhood: Dict[str, np.ndarray] = {word: word_embedding}
        index = faiss.IndexFlatIP(300)  # inner product, i.e., cosine similarity
        index.add(np.ascontiguousarray(self.attractrepelled_numberbatch))
        _, neighbors_idxs = index.search(np.array(word_embedding, dtype=np.float32), nearest_k)
        # neighbors_names: List[str] = [self.attractrepelled_numberbatch_words[i] for i in neighbors_idxs]
        # neighbors_embeddings: np.ndarray = self.attractrepelled_numberbatch_embeddings[neighbors_idxs]
        for i in neighbors_idxs:
            i = int(i)  # convert numpy.int64 to int
            neighborhood[self.attractrepelled_numberbatch_words[i]] = self.attractrepelled_numberbatch_embeddings[i, :]
        return neighborhood

    # TODO
    #   Add normalization functions for DRD outputs.

    def getBestRelation(self, word1: str, word2: str) -> Dict[str, Union[str, float]]:
        # word1_embedding: tf.Tensor = tf.convert_to_tensor(
        #     value=self.getWordEmbedding(word1),
        #     dtype=tf.float32,
        #     name='retro_word_1'
        # )
        # word2_embedding: tf.Tensor = tf.convert_to_tensor(
        #     value=self.getWordEmbedding(word2),
        #     dtype=tf.float32,
        #     name='retro_word_2'
        # )
        result = {'word1': word1, 'rel': '', 'word2': word2, 'weight': 0.0}
        word1_embedding: np.ndarray = self.getWordEmbedding(word1)
        word2_embedding: np.ndarray = self.getWordEmbedding(word2)
        # TODO: For now, don't worry about neighborhood
        best_relation_name = ''
        best_relation_weight = np.float32(-100.0)
        for relation_name, model in self.drd_models.items():
            relation_weight: List[np.ndarray] = model.predict(
                x={
                    'retro_word_1': word1_embedding.reshape(1, 300),
                    'retro_word_2': word2_embedding.reshape(1, 300)
                }
            )  # [1-by-1 np.ndarray, 1-by-1 np.ndarray]
            ## For now, I will use score, which, although unnormalized, seems like a more warranted
            ## measure of the commonsense semantics that has been extracted from ConceptNet.
            ## - YDX@20210311
            # FIXME
            #   relation_weight: np.float32 = relation_weight[0][0][0]  # probability
            relation_weight: np.float32 = relation_weight[1][0][0]  # score
            if best_relation_weight < relation_weight:
                best_relation_name = relation_name
                best_relation_weight = relation_weight
        result['rel'] = best_relation_name
        result['weight'] = best_relation_weight
        return result
