from typing import List, Dict, Any, Union, Optional
import requests
from urllib.parse import urlencode


class ConceptnetQueryer:
    # def __init__(self, concept1: str = '', concept2: str = '', relation: str = ''):
    #     self.concept1 = concept1
    #     self.concept2 = concept2
    #     self.relation = relation

    def __init__(self):
        pass

    def _addConceptIdentifier(self, concept_name: str) -> str:
        if '/c/en/' not in concept_name:
            concept_name = f'/c/en/{concept_name}'
        return concept_name

    def _addRelationIdentifier(self, relation_name: str) -> str:
        if relation_name[0].islower():
            relation_name = relation_name[0].upper() + relation_name[1:]
        if '/r/' not in relation_name:
            relation_name = f'/r/{relation_name}'
        return relation_name

    def queryConceptnet(self, concept1: str, concept2: str = '', relation: str = '') -> Dict[str, Any]:
        temp = {'node': self._addConceptIdentifier(concept1.lower())}
        if concept2 != '':
            temp['other'] = self._addConceptIdentifier(concept2.lower())
        if relation != '':
            temp['rel'] = self._addRelationIdentifier(relation.lower())
        ## This is where all the "magic" takes place
        url = f'http://api.conceptnet.io/query?{urlencode(temp)}'
        return requests.get(url=url, timeout=10).json()

    def getBestRelation(self, word1: str, word2: str) -> Optional[Dict[str, Union[str, float]]]:
        # TODO (Alvin & Yida)
        #   !!! Need better ways to get the best relations from ConceptNet !!!
        """
        Description:
            Given two concepts, we want to query ConceptNet and find the
            "best" relation inside ConceptNet that connects these concepts.
            The best relation is the one with the highest weight --- a very
            naive notion of "best".
        Arguments:
            - Two concepts
        Returns:
            - Name of the best relation
            - Weight of the best relation
        Note:
            For downstream numerical tasks, we only care about the weight;
            for understanding the meaning of weight, the name of relation
            is very important.
        """
        ## Send get request to ConceptNet API
        results = self.queryConceptnet(concept1=word1, concept2=word2)
        if not results['edges']:
            return {
                'start': '',
                'rel': '',
                'end': '',
                'weight': 0.0
            }
        ## Customize each edge into a simpler dict
        assertions: List[Dict[str, Union[str, float]]] = [{
            'start': x['start']['label'].split(' ')[-1],
            'rel': x['rel']['label'].split(' ')[-1],
            'end': x['end']['label'].split(' ')[-1],
            'weight': x['weight']
        } for x in results['edges']]
        ## Sort by weight
        assertions = sorted(assertions, key=lambda x: x['weight'])
        ## Return the assertion with largest weight (i.e., the last one)
        return assertions[-1]
