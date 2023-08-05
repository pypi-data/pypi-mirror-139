from typing import List, Dict, Optional, Any
# import argparse
import spacy
# import neuralcoref
from spacy.lang.en import English
from spacy.tokens import Doc, Token
from .conceptnet_queryer import ConceptnetQueryer
# from patchcomm.models.retrogan_drd_queryer import RetroganDrdQueryer
# from src.patchcomm.models.start_queryer import StartParserQueryer
from .pp_attacher import PrepositionalPhraseAttacher
from .coref_resolver import CoreferenceResolver


#########################################################################
##                                                                     ##
## spaCy resources; use spacy.explain() to see the explanation of each ##
##                                                                     ##
#########################################################################

## All values of token.pos_
## Source: https://spacy.io/api/annotation#pos-tagging ---> "Universal Part-of-speech Tags"
ALL_SPACY_UNIVERSAL_POS_TAGS = [
    'ADJ', 'ADP', 'ADV', 'AUX', 'CONJ', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'NUM', 'PRON', 'PROPN', 'PUNCT',
    'SCONJ', 'SYM', 'VERB', 'X', 'SPACE'
]

## All values of token.dep_
## Source: https://spacy.io/models/en#en_core_web_lg --> "Label Schemes" --> "PARSER"
## Source: https://spacy.io/api/annotation#dependency-parsing ---> "Universal Dependency Labels"
ALL_SPACY_SYNTACTIC_DEPENDENCY_LABELS = [
    'ROOT', 'acl', 'acomp', 'advcl', 'advmod', 'agent', 'amod', 'appos', 'attr', 'aux', 'auxpass', 'case', 'cc',
    'ccomp', 'compound', 'conj', 'csubj', 'csubjpass', 'dative', 'dep', 'det', 'dobj', 'expl', 'intj', 'mark',
    'meta', 'neg', 'nmod', 'npadvmod', 'nsubj', 'nsubjpass', 'nummod', 'oprd', 'parataxis', 'pcomp', 'pobj',
    'poss', 'preconj', 'predet', 'prep', 'prt', 'punct', 'quantmod', 'relcl', 'xcomp'
]

## All values of token.ent_type_
## Source: https://spacy.io/api/annotation#named-entities
ALL_SPACY_ENTITY_TYPES = [
    'PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE',
    'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL'
]


# TODO
#   1. Define a class that defaults to spaCy token.head if it's not informed by any external knowledge,
#       but makes informed decision when informed externally.
#   2. Define a class that creates a mapping between START syntactic labels and spaCy syntactic labels.
#       Then, within the same class, translate a sentence's START *final* parse into spaCy *final* parse.
#       Then, manipulate the final parse, as opposed to some sort of partial parse that we don't have.


class SentenceParser:
    def __init__(self):
        self.nlp: English = spacy.load('en_core_web_lg')
        ## Try using NeuralCoref.  However, when we use spaCy v3.2.1, NeuralCoref will no longer work,
        ## so we must catch the exception here.
        self.use_neuralcoref = False
        try:
            import neuralcoref
            neuralcoref.add_to_pipe(self.nlp)
            self.use_neuralcoref = True
        except ValueError as e:
            print(e)
        ## ConceptNet and RetroGAN-DRD Queryers
        self.conceptnet_queryer = ConceptnetQueryer()
        # self.retrogan_drd_queryer = RetroganDrdQueryer()  # TODO: not ready for RetroGAN-DRD yet
        # ## START stuff
        # self.start_parser_queryer = StartParserQueryer(server='genesis', machine='malta')
        ## PP Attachment Resolver
        self.ppattach_resolver = PrepositionalPhraseAttacher(conceptnet_queryer=self.conceptnet_queryer)
        ## Coref Resolver
        self.coref_resolver = CoreferenceResolver(use_neuralcoref=self.use_neuralcoref, conceptnet_queryer=self.conceptnet_queryer)

    # TODO (long-term)
    #   There is a possibility to return to START work later somewhere down the road.
    #   For now, I have ceased working on/with START.
    # ###########
    # ##       ##
    # ## START ##
    # ##       ##
    # ###########
    #
    # def getStartParse(self, sentence: str, use_conceptnet: bool, use_retrogan_drd: bool) -> List[List[str]]:
    #     """
    #     Take the entirety of start triples as provided by StartParserQueryer.getTriples(), and focus on
    #     only those triples where the relation is preposition ("ADP" by spaCy).
    #
    #     For such triples, the object is the root of the prepositional phrase.  For example, if the triple
    #     is [like+1 with+1 cheese+2495], then the prepositional phrase is (with+1, cheese+2495).
    #
    #     If ConceptNet gives a different decision, e.g. "pizza with cheese" instead of "like with cheese",
    #     then change the triple from [like+1 with+1 cheese+2495] to [pizza+2494 with+1 cheese+2495].
    #
    #     If there are more than one such triples to process, then process each in the same way.
    #     """
    #     start_triples: List[List[str]] = self.start_parser_queryer.getStartTriples(sentence=sentence)
    #     start_tokens: List[str] = self.start_parser_queryer.getStartTokens(sentence=sentence)
    #     parsed: List[List[str]] = start_triples
    #     doc: Doc = self.nlp(sentence)
    #     ####################
    #     ##                ##
    #     ## PPAttach Stuff ##
    #     ##                ##
    #     ####################
    #     # TODO (YDX@20210311)
    #     #   For now, use only ConceptNet -- especially for tomorrow Genesis's demo!
    #     #   For the future, use both ConceptNet and DRD, compare these two, and use the better one.
    #     # ppattach_decisions = self._getAttachmentsUsingConceptnet(doc=doc)
    #     ppattach_decisions = self.ppattach_resolver.getAttachments(
    #         doc=doc,
    #         use_conceptnet=use_conceptnet,
    #         use_retrogan_drd=use_retrogan_drd
    #     )['ConceptNet decisions']
    #     if ppattach_decisions is not None:
    #         ppattach_decisions_keys: List[Token] = list(ppattach_decisions.keys())
    #         for triple in parsed:
    #             relation_token: Token = self.nlp(triple[1].split('+')[0])[0]  # spaCy token
    #             object_token: Token = self.nlp(triple[2].split('+')[0])[0]  # spaCy token
    #             if relation_token.pos_ == 'ADP':
    #                 for i in range(len(ppattach_decisions_keys)):
    #                     if object_token.text == ppattach_decisions_keys[i].text:
    #                         object_token_correspondent = ppattach_decisions_keys[i]
    #                 for t in start_tokens:  # !!! START tokens are strings, not spaCy tokens !!!
    #                     if ppattach_decisions[object_token_correspondent].lemma_ in t:
    #                         triple[0] = t
    #     #################
    #     ##             ##
    #     ## Coref Stuff ##
    #     ##             ##
    #     #################
    #     # TODO: !!! Add coref stuff ASAP !!!
    #
    #     return parsed

    #########################
    ##                     ##
    ## spaCy & NeuralCoref ##
    ##                     ##
    #########################

    def getSpacyParse(
            self,
            sentence: str,
            use_conceptnet: bool,
            use_retrogan_drd: bool,
            use_lemma=False
    ) -> Dict[str, Optional[Any]]:
        doc: Doc = self.nlp(sentence)
        ## Set up template for final parsed
        parsed = {
            'words': [],
            'arcs': [],
            'settings': {'lang': 'en', 'direction': 'ltr'}
        }
        ## Get all PP attachment stuff
        prepositional_phrases: List[List[Token]] = self.ppattach_resolver.getPPs(doc=doc)
        ambiguous_ppattachs: Dict[Token, List[Token]] = self.ppattach_resolver.getAmbiguousPPAttachs(doc=doc)
        ppattach_decisions: Dict[str, Dict[Token, Token]] = self.ppattach_resolver.getAttachments(
            doc=doc,
            use_conceptnet=use_conceptnet,
            use_retrogan_drd=use_retrogan_drd
        )
        # TODO: not ready to use RetroGAN-DRD yet
        if ppattach_decisions:
            ppattach_decisions: Dict[Token, Token] = ppattach_decisions['ConceptNet decisions']
            # ppattach_conceptnet_decisions: Dict[Token, Token] = ppattach_decisions['ConceptNet decisions']
            # ppattach_retrogan_drd_decisions: Dict[Token, Token] = ppattach_decisions['RetroGAN-DRD decisions']
        ## Get all coreference stuff
        pronouns: List[Token] = self.coref_resolver.getPronouns(doc=doc)
        coref_resolutions: Dict[str, Dict[Token, Token]] = self.coref_resolver.getCorefResolutions(
            doc=doc,
            use_conceptnet=use_conceptnet,
            use_retrogan_drd=use_retrogan_drd
        )
        # TODO: not ready to use RetroGAN-DRD yet
        if coref_resolutions:
            coref_resolutions: Dict[Token, Token] = coref_resolutions['ConceptNet resolutions']
            # coref_conceptnet_resolutions: Dict[Token, Token] = coref_resolutions['ConceptNet resolutions']
            # coref_retrogan_drd_resolutions: Dict[Token, Token] = coref_resolutions['RetroGAN-DRD resolutions']
        # TODO (long-term)
        #   Instead of changing the arrows in the original spaCy parse, add another arrow from preposition
        #   to the verb or noun where the prep-phrase is supposed to be attached, with label "prep-attach"
        for token in doc:
            child = token
            head = token.head
            ####################
            ##                ##
            ## PPAttach Stuff ##
            ##                ##
            ####################
            ## Add words
            parsed['words'].append({
                'text': child.text,
                'tag': child.pos_,
                'lemma': child.lemma_ if use_lemma is True else None
            })
            ## Add arcs
            if child.dep_ == 'prep':
                if child.text not in self.ppattach_resolver.accepted_preps:
                    if child.i < head.i:
                        parsed['arcs'].append({
                            'start': child.i,
                            'end': head.i,
                            'label': child.dep_,
                            'dir': 'left'
                        })
                    elif child.i > head.i:
                        parsed['arcs'].append({
                            'start': head.i,
                            'end': child.i,
                            'label': child.dep_,
                            'dir': 'right'
                        })
                else:
                    continue
            elif ambiguous_ppattachs is not None \
                    and child in list(ambiguous_ppattachs.keys()) \
                    and ppattach_decisions is not None:
                for prep_phrase in prepositional_phrases:
                    if child in prep_phrase:
                        child_prep = self.ppattach_resolver.getPrepFromPP(prep_phrase)
                child_prep_attach: Token = ppattach_decisions[child]
                parsed['arcs'].append({
                    'start': child_prep_attach.i if child_prep_attach is not None else child_prep.head.i,
                    'end': child_prep.i,
                    'label': child_prep.dep_,
                    'dir': 'right'
                })
                parsed['arcs'].append({
                    'start': child_prep.i,
                    'end': child.i,
                    'label': child.dep_,
                    'dir': 'left'
                })
            elif child.i < head.i:
                parsed['arcs'].append({
                    'start': child.i,
                    'end': head.i,
                    'label': child.dep_,
                    'dir': 'left'
                })
            elif child.i > head.i:
                parsed['arcs'].append({
                    'start': head.i,
                    'end': child.i,
                    'label': child.dep_,
                    'dir': 'right'
                })
            #################
            ##             ##
            ## Coref Stuff ##
            ##             ##
            #################
            if pronouns and coref_resolutions:
                for pronoun, coref in coref_resolutions.items():
                    if (child == pronoun) and (coref is not None):
                        if child.i > coref.i:
                            parsed['arcs'].append({
                                'start': coref.i,
                                'end': child.i,
                                'label': 'coref',
                                'dir': 'right'
                            })
                        else:
                            parsed['arcs'].append({
                                'start': child.i,
                                'end': coref.i,
                                'label': 'coref',
                                'dir': 'right'
                            })
        return parsed


# ========== DEMO CODE BELOW (for Genesis meeting) ==========
#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         '--ppattach_sentence',
#         default='John plays his guitar with two strings in his chair',
#         help='a sentence for demonstrating how prepositional-phrase attachment ambiguity is resolved'
#     )
#     parser.add_argument(
#         '--coref_sentence',
#         default='The knife cut through the butter because it was sufficiently hard',
#         help='a sentence for demonstrating how pronoun co-reference ambiguity is resolved'
#     )
#     parser.add_argument(
#         '--use_conceptnet',
#         default=True,
#         help='whether to use ConceptNet as external knowledge source (default: True)'
#     )
#     parser.add_argument(
#         '--use_retrogan_drd',
#         default=False,
#         help='whether to use RetroGAN-DRD as external knowledge source (default: False)'
#     )
#
#     params = parser.parse_args()
#
#     # ppattach_sentence = params.ppattach_sentence
#     # coref_sentence = params.coref_sentence
#     use_conceptnet = params.use_conceptnet
#     use_retrogan_drd = params.use_retrogan_drd
#     start = StartParserQueryer()
#     demo_parser = SentenceParser()
#     while True:
#         try:
#             print('')
#             print('+-------------------------------+')
#             print('| Demo: PP Attachment Ambiguity |')
#             print('+-------------------------------+')
#             sentence = str(input('Type a sentence: '))
#             print('\n==========\n')
#             print('Original START parse:')
#             for x in start.getStartTriples(sentence):
#                 print(x)
#             print('')
#             print('Improved START parse:')
#             for x in demo_parser.getStartParse(sentence, use_conceptnet, use_retrogan_drd):
#                 print(x)
#             print('')
#             print('+--------------------------------------+')
#             print('| Demo: Pronoun Co-reference Ambiguity |')
#             print('+--------------------------------------+')
#             sentence = str(input('Type a sentence: '))
#             print('\n==========\n')
#             print('Original START parse:')
#             from patchcomm.models.start_queryer import StartParserQueryer
#             start = StartParserQueryer()
#             for x in start.getStartTriples(sentence):
#                 print(x)
#             print('')
#             print('Improved START parse:')
#             for x in demo_parser.getStartParse(sentence, use_conceptnet, use_retrogan_drd):
#                 print(x)
#         except KeyboardInterrupt:
#             break
