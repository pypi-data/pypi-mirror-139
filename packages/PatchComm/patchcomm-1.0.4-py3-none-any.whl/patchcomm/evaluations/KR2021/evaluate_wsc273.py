from typing import Dict, List, Any
import time
from xml.etree import ElementTree
import xmltodict
# import json
import spacy
from spacy.tokens import Doc, Token
from src.patchcomm.models.conceptnet_queryer import ConceptnetQueryer
import neuralcoref
from neuralcoref.neuralcoref import Cluster


nlp = spacy.load('en_core_web_lg')
neuralcoref.add_to_pipe(nlp)
cn_queryer = ConceptnetQueryer()


def loadWSC(source: str = 'src/patchcomm/data/winograd_schema/WSC285.xml') -> List[Dict[str, Any]]:
    ## Read and parse the XML data
    wsc_xml = ElementTree.parse(source=source).getroot()
    wsc_xml = ElementTree.tostring(wsc_xml, encoding='utf-8', method='xml')
    ## Convert XML to OrderedDict
    wsc_ordereddict = xmltodict.parse(wsc_xml)
    ## Convert OrderedDict to Dict
    wsc: List[Dict[str, Any]] = dict(dict(wsc_ordereddict)['collection'])['schema']
    for i in range(len(wsc)):
        wsc[i] = dict(wsc[i])
        wsc[i]['text'] = dict(wsc[i]['text'])
        wsc[i]['quote'] = dict(wsc[i]['quote'])
        wsc[i]['answers'] = dict(wsc[i]['answers'])
    return wsc


def preprocessWSC(wsc_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Change data structure from

        {
            'text': {
                'txt1': 'The delivery truck zoomed by the school bus because',
                'pron': 'it',
                'txt2': 'was going so fast.'
            },
            'quote': {
                'pron': 'it',
                'quote2': 'was going so fast.'
            },
            'answers': {'answer': ['the delivery truck', 'the school bus']},
            'correctAnswer': 'A.',
            'source': 'Hector Levesque'
        }

    to

        {
            'text': 'The delivery truck zoomed by the school bus because it was going so fast.',
            'pronoun': 'it'
            'candidates': ['truck', 'bus']
            'answer': {'it': 'truck'}
        }
    """

    def _getPhraseRoot(phrase: str) -> str:
        """Takes a phrase (e.g., 'the delivery truck') and returns its root (e.g., 'truck')"""
        return [t for t in nlp(phrase) if t.dep_ == 'ROOT'][0].text

    for x in wsc_data:
        pronoun = x['text']['pron']
        ## Add 'text'
        x['text'] = f"{x['text']['txt1']} {pronoun} {x['text']['txt2']}"
        ## Add 'pronoun'
        x['pronoun'] = pronoun
        ## Add 'candidates'
        candidates: List[str] = [_getPhraseRoot(p) for p in x['answers']['answer']]
        x['candidates'] = candidates
        ## Add 'answer'
        if x['correctAnswer'][0] == 'A':
            x['answer'] = {pronoun: candidates[0]}
        else:
            x['answer'] = {pronoun: candidates[1]}
        ## Delete the dictionary entries that we no longer need
        del x['quote']
        del x['answers']
        del x['correctAnswer']
        del x['source']

    return wsc_data


def getCorefUsingConceptnet(wsc: Dict[str, Any]) -> Dict[str, str]:
    """
    Recall that wsc looks like
    {
        'text': 'The delivery truck zoomed by the school bus because it was going so fast.',
        'pronoun': 'it'
        'candidates': ['truck', 'bus']
        'answer': {'it': 'truck'}
    }
    """
    ## First get everything from wsc
    doc: Doc = nlp(wsc['text'])
    pronoun: str = wsc['pronoun']
    candidates: List[str] = wsc['candidates']  # len == 2
    ## Next use doc to process
    candidates_tokens: List[Token] = []
    ## Get pronoun token
    pronoun_token = [x for x in doc if x.text == pronoun][0]
    for x in doc:
        ## Get token that describes pronoun
        if x.head == pronoun_token.head and x.pos_ != 'SCONJ':
            description_token = x
        ## Get candidate tokens
        elif x.text in candidates:
            candidates_tokens.append(x)
    ## Use ConceptNet
    max_weight: float = -100.0
    for candidate in candidates_tokens:
        weight = cn_queryer.getBestRelation(
            word1=candidate.text,
            word2=description_token.text
        )['weight']
        if max_weight < weight:
            max_weight = weight
            coref: str = candidate.text
    return {pronoun: coref}


# def evaluateAgainstNeuralcoref(wsc: Dict[str, Any]) -> Dict[str, bool]:
#     doc = nlp(wsc['text'])
#     ## Get ground truth
#     ground_truth: Dict[str, str] = wsc['answer']
#     ## Get NeuralCoref answer
#     neuralcoref_answer: Dict[str, str] = {doc._.coref_clusters[0][1][-1].text: doc._.coref_clusters[0][0][-1].text}
#     ## Get PatchComm answer
#     patchcomm_answer: Dict[str, str] = getCorefUsingConceptnet(wsc)
#     ## Compare neuralcoref_answer with ground_truth
#     ## Compare patchcomm_answer with ground_truth
#     ## Return statistics
#     return {
#         'neuralcoref': neuralcoref_answer == ground_truth,
#         'patchcomm': patchcomm_answer == ground_truth
#     }


def evaluate() -> Dict[str, float]:
    ## Load and preprocess WSC273 instead of WSC285
    # all_wsc: List[Dict[str, Any]] = preprocessWSC(loadWSC())[:273]  # all original WSC273 sentences
    # all_wsc: List[Dict[str, Any]] = preprocessWSC(loadWSC())[:100]  # do only first 100 sentences, for time comparisons
    all_wsc: List[Dict[str, Any]] = preprocessWSC(loadWSC())[:273]
    all_wsc = all_wsc + all_wsc  # do the sentences twice, for time comparisons
    ## Evaluate on WSC273
    total_correct_neuralcoref: int = 0
    total_correct_patchcomm: int = 0
    n_diff: int = 0
    total_conceptnet_time: float = 0.0
    for wsc in all_wsc:
        ## Get ground truth
        ground_truth: Dict[str, str] = wsc['answer']
        ## Get NeuralCoref answer
        neuralcoref_clusters: Cluster = nlp(wsc['text'])._.coref_clusters
        if neuralcoref_clusters:
            neuralcoref_answer = {
                neuralcoref_clusters[0][1][-1].text: neuralcoref_clusters[0][0][-1].text
            }
        else:
            neuralcoref_answer = None
        ## Get PatchComm answer
        start_time = time.time()
        patchcomm_answer = getCorefUsingConceptnet(wsc)
        end_time = time.time()
        total_conceptnet_time += (end_time - start_time)
        ## Analysis
        if neuralcoref_answer is not None:
            if neuralcoref_answer == ground_truth:
                total_correct_neuralcoref += 1
                # print(f'neuralcoref right: #{all_wsc.index(wsc)}')  # !!! GET BACK !!!
        else:
            # print(f'neuralcoref none: #{all_wsc.index(wsc)}')  # !!! GET BACK !!!
            pass
        if patchcomm_answer == ground_truth:
            total_correct_patchcomm += 1
            # print(f'patchcomm right: #{all_wsc.index(wsc)}')  # !!! GET BACK !!!
        if patchcomm_answer != neuralcoref_answer:
            n_diff += 1
            # print(f'which diff: #{all_wsc.index(wsc)}')  # !!! GET BACK !!!
        # ## Log some info for human
        # i = all_wsc.index(wsc)
        # if i % 20 == 0:
        #     print(f'WSC #{i} passed')
    percent_correct_neuralcoref: float = total_correct_neuralcoref / len(all_wsc)
    percent_correct_patchcomm: float = total_correct_patchcomm / len(all_wsc)
    percent_diff: float = n_diff / len(all_wsc)
    print(f'getCorefUsingConceptNet() took {total_conceptnet_time:.2f} seconds in total')
    return {
        'NeuralCoref %': percent_correct_neuralcoref,
        'PatchComm %': percent_correct_patchcomm,
        'diff %': percent_diff
    }
