"""
PySTART has already implemented send_request() and parse().

However, because the InfoLab group sometimes have machines not working or server shut off,
I have decided to reimplement send_request() and parse() so that I can independently specify
server and machine, and change them whenever necessary.

ydx@2021-02-16
"""

from typing import List, Dict, Optional, Any
import requests
import xmltodict
from pystart.start import recur_ordereddict_to_dict, get_body


class StartParserQueryer:
    def __init__(self, server='genesis', machine='fiji'):
        self.pystart_referrer_url = 'http://start.csail.mit.edu/pystart'
        self.start_api_url = 'http://start.csail.mit.edu/api.php'
        self.server = server
        self.machine = machine

    def getStartInitialParse(self, sentence):
        params: Dict[str, str] = {
            'referrer': self.pystart_referrer_url,
            'query': sentence,
            'action': 'parse',
            'server': self.server,
            'machine': self.machine,
            'qe': 'HTML',
            'kb': 'no',
            'te': 'XML',
            'de': 'no',
            'fg': 'yes',
            'cd': 'no'
        }
        r = requests.post(url=self.start_api_url, data=params)
        try:
            response = recur_ordereddict_to_dict(xmltodict.parse(r.text))
        except xmltodict.expat.ExpatError:
            raise ValueError('!!! Failed to connect to a good START machine !!!')
        reply = get_body(response, 'reply')
        if 'texp' in reply:
            return list(reply['texp'])
        return None

    def getStartTriples(self, sentence):
        """
        Converts the list of all START's original triples into a list of lists
        """
        def _getEntity(stuff):
            if 'constant' in stuff:
                return stuff['constant']
            elif 'instance' in stuff:
                return f"{stuff['instance']['#text']}+{stuff['instance']['@index']}"
        def _peelRecursively(data):
            """
            Base case is where both subject and object are either 'constant' or 'instance';
            inductive case is where either subject or object -- or both -- is 'texp'
            """
            if ('constant' in data['subject'] or 'instance' in data['subject']) \
                    and ('constant' in data['object'] or 'instance' in data['object']):
                return [
                    _getEntity(data['subject']),
                    _getEntity(data['relation']),
                    _getEntity(data['object'])
                ]
            elif 'texp' in data['subject'] \
                    and ('constant' in data['object'] or 'instance' in data['object']):
                return [
                    _peelRecursively(data['subject']['texp'])[1],
                    _getEntity(data['relation']),
                    _getEntity(data['object'])
                ]
            elif ('constant' in data['subject'] or 'instance' in data['subject']) \
                    and 'texp' in data['object']:
                return [
                    _getEntity(data['subject']),
                    _getEntity(data['relation']),
                    _peelRecursively(data['object']['texp'])[1]
                ]
            elif 'texp' in data['subject'] and 'texp' in data['object']:
                return [
                    _peelRecursively(data['subject']['texp'])[1],
                    _getEntity(data['relation']),
                    _peelRecursively(data['object']['texp'])[1]
                ]
        return [_peelRecursively(x) for x in self.getStartInitialParse(sentence=sentence)]

    def getStartTokens(self, sentence):
        """
        (!!! Not sure how this function is useful, yet !!!)
        Goes through the list of all START's triples, and stores all the nonredundant tokens
        into a list.
        """
        start_tokens: List[str] = []
        for triple in self.getStartTriples(sentence=sentence):
            for x in triple:
                if x not in start_tokens:
                    start_tokens.append(x)
        return start_tokens
