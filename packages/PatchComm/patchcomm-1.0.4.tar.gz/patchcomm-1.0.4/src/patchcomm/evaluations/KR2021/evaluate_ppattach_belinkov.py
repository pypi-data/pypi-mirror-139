from typing import Dict, List
import time
import json
import spacy
from spacy.tokens import Doc, Token
from src.patchcomm.models.conceptnet_queryer import ConceptnetQueryer


nlp = spacy.load('en_core_web_lg')
cn_queryer = ConceptnetQueryer()


# TODO (!!! immediately !!!)
#   + Finish preparing sentences.txt file
#   - Specialize the PP Attachment Resolver to KR2021
#   - Make cn_queryer do multi-step search (!!! NOT ENOUGH TIME GOD FUCKING DAMN IT !!!)
#   + Add lemma_ usage to concept queryer


def loadBelinkov(path: str = 'src/patchcomm/data/self-created/sentences.txt') -> List[str]:
    with open(path, 'r') as f:
        sentences: List[str] = [x for x in f.read().strip().split('\n') if x != '']
    return sentences


def getAttachmentUsingConceptnet(sentence: str) -> Dict[str, str]:
    """
    Recall that patch looks like
    {
        'text': 'The person saved the bird with one arm',
        'answer': {'arm': 'saved'}
    }
    or
    {
        'text': 'The person saved the bird with one wing',
        'answer': {'wing': 'bird'}
    }
    """
    # print(sentence)
    doc: Doc = nlp(sentence)
    pobj: str = [x for x in doc if x.dep_ == 'pobj'][0].text
    subj: str = [x for x in doc if x.dep_ == 'nsubj'][0].text
    verb: str = [x for x in doc if x.dep_ == 'ROOT'][0].text
    prep_token: Token = [x for x in doc if x.dep_ == 'prep'][0]
    noun1: str = [x for x in doc if x.pos_ == 'NOUN' and x.text != subj and x.i < prep_token.i][0].text
    # print(f'verb == {verb}')
    # print(f'noun1 == {noun1}')
    # print(f'pobj == {pobj}')
    ## Use ConceptNet
    weight1: float = max(  # for weight 1, do (V, pobj) and (subj, pobj)
        cn_queryer.getBestRelation(verb, pobj)['weight'],
        cn_queryer.getBestRelation(subj, pobj)['weight']
    )
    # print(f'weight1 == {weight1}')
    weight2 = cn_queryer.getBestRelation(noun1, pobj)['weight']
    # print(f'weight2 == {weight2}')
    if weight1 == 0.0 and weight2 == 0.0:
        # print('here1\n')
        return {pobj: prep_token.head.text}
    elif weight1 == 0.0 and weight2 > 0.0:
        # print('here2\n')
        return {pobj: noun1}
    elif weight1 > 0.0 and weight2 == 0.0:
        # print('here3\n')
        return {pobj: verb}
    else:
        if weight1 > weight2:
            # print('here4\n')
            return {pobj: verb}
        else:
            # print('here5\n')
            return {pobj: noun1}


def evaluate() -> Dict[str, float]:
    total_correct_spacy: int = 0
    total_correct_patchcomm: int = 0
    n_diff: int = 0
    total_conceptnet_time: float = 0.0
    ## Load and preprocess ppattach dataset
    with open('src/patchcomm/data/self-created/sentences.txt') as f:
        # lines = [x for x in f.read().strip().split('\n') if x != '']  # all 100 sentences
        # lines = [x for x in f.read().strip().split('\n') if x != ''][:50]  # do only first 50 sentences, for time comparisons
        lines = [x for x in f.read().strip().split('\n') if x != '']
        lines = lines + lines  # do the sentences twice, for time comparisons
    data = list(zip(lines[0::2], lines[1::2]))
    for sentence, answer in data:
        # data = {'text': text, 'answer': json.loads(answer)}
        # all_data.append(data)
        ## Get ground truth
        ground_truth = json.loads(answer)
        ## Get spaCy answer
        doc = nlp(sentence)
        spacy_answer = {
            [x for x in doc if x.dep_ == 'pobj'][0].text: [x.head for x in doc if x.dep_ == 'prep'][0].text
        }
        ## Get PatchComm answer
        start_time = time.time()
        patchcomm_answer = getAttachmentUsingConceptnet(sentence)
        end_time = time.time()
        total_conceptnet_time += (end_time - start_time)
        ## Analysis
        if spacy_answer == ground_truth:
            total_correct_spacy += 1
            # total_correct_patchcomm += 1
        if patchcomm_answer == ground_truth:
            total_correct_patchcomm += 1
        if spacy_answer != patchcomm_answer:
            n_diff += 1
        # print(f'spaCy answer: {spacy_answer} | {spacy_answer == ground_truth}')
        # print(f'PatchComm answer: {patchcomm_answer} | {patchcomm_answer == ground_truth}')
        # print('')
        ## Log some info for human
        i = data.index((sentence, answer))
        # if i % 20 == 0:
        #     print(f'ppattach #{i} passed')  # !!! GET BACK !!!
    percent_correct_spacy: float = total_correct_spacy / len(data)
    percent_correct_patchcomm: float = total_correct_patchcomm / len(data)
    percent_diff: float = n_diff / len(data)
    print(f'getAttachmentUsingConceptNet() took {total_conceptnet_time:.2f} seconds in total')
    return {
        'spaCy %': percent_correct_spacy,
        'PatchComm %': percent_correct_patchcomm,
        'diff %': percent_diff
    }
