from typing import List, Dict, Tuple, Optional, Any
from spacy.tokens import Token, Doc


class CoreferenceResolver:
    """
    Lending an ear to WSC again, I want to build a sentence-level Coreference Resolution system that takes on
    the Winograd Schema Challenge and its descendants.

    This coref resolver needs to deal, for now, the problem setting specified by Levesque et al.
      - Exactly two parties are mentioned
      - A pronoun -- definite or indefinite -- or its possessive form is used to refer to either, but not both,
        of the two parties
      - There is an adjective that unambiguously describes the one party -- the referent of interest -- without
        describing the other party

    e.g.,
      - The trophy does not fit the brown suitcase because [it] is too large.  What is too large?
      - The trophy does not fit the brown suitcase because [it] is too small.  What is too small?

    This coref resolver needs to be implemented as such:
      - use spaCy to obtain the parts of speech and the dependency parse
      - obtain the 2 nouns and the 1 adjective
      - use ConceptNet to determine which of the 2 nouns this adjective describes; change dependency parse if needed
      - spaCy should already have the pronoun pointing at the adjective, but check whether this is the case;
        if so, simply trace from the pronoun to the adjective and then to the noun, hence resolving the coreference
    """
    def __init__(self, use_neuralcoref, conceptnet_queryer=None, retrogan_drd_queryer=None):
        # # TODO (Immediately):
        # #   As PatchComm moves from spaCy 2.3.5 to spaCy 3.2.1, NeuralCoref no longer works.
        # #   Instead, we will use the work of Coreference Resolutions Without Span Representations
        # #   (see https://github.com/yuvalkirstain/s2e-coref).
        # self.use_neuralcoref = False
        # if base_coref_resolver == '':
        #     pass
        # elif base_coref_resolver.lower() == 'neuralcoref':
        #     self.use_neuralcoref = True
        self.pronouns = [
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'us', 'them', 'him',
            'my', 'your', 'his', 'her', 'its', 'our', 'their',
            'mine', 'yours', 'hers', 'ours', 'theirs'
        ]
        self.non_pronouns = [
            'who', 'whom', 'whose'
        ]
        self.use_neuralcoref = use_neuralcoref
        if conceptnet_queryer is not None:
            self.conceptnet_queryer = conceptnet_queryer
        if retrogan_drd_queryer is not None:
            self.retrogan_drd_queryer = retrogan_drd_queryer

    #################################
    ##                             ##
    ## NeuralCoref stuff (default) ##
    ##                             ##
    #################################

    def getNeuralcorefPronouns(self, doc: Doc) -> List[Token]:
        if self.use_neuralcoref:
            return [x[1][-1] for x in doc._.coref_clusters]
        return []  # FIXME: return empty list for now

    def getNeuralcorefResolutions(self, doc: Doc) -> Dict[Token, Token]:
        """
        See https://github.com/huggingface/neuralcoref/blob/master/neuralcoref/neuralcoref.pyx
        Go to class `Cluster` on line 454 (as of April 20, 2021)
        """
        if self.use_neuralcoref:
            return {x[1][-1]: x[0][-1] for x in doc._.coref_clusters}
        return {}  # FIXME: return empty dict for now

    #####################
    ##                 ##
    ## PatchComm stuff ##
    ##                 ##
    #####################

    def getPronouns(self, doc: Doc) -> Optional[List[Token]]:
        """
        By default, we assume all pronouns are ambiguous, therefore, we get
        a list of all pronouns in the sentence
        """
        return [
            token for token in doc
            if (((token.pos_ == 'PRON' and token.dep_ != 'expl')
                 or (token.text.lower() in self.pronouns))
                and (token.text.lower() not in self.non_pronouns))
        ]

    # def getAmbiguousPronounsDescriptions(self, doc: Doc) -> Optional[List[Tuple[Token, Token]]]:
    #     """
    #     Very naively, what we consider to be a *description* of the ambiguous pronoun,
    #     is the token in the sentence that share the same head with the ambiguous pronoun.
    #     e.g., for the sentence "The knife cut the butter because it was soft", the description
    #     for the ambiguous pronoun, "it", is "soft", because they share the same head, "was".
    #     """
    #     ambiguous_pronouns: Optional[List[Token]] = self.getAmbiguousPronouns(doc=doc)
    #     results: List[Tuple[Token, Token]] = []
    #     if not ambiguous_pronouns:
    #         return None
    #     for ambiguous_pronoun in ambiguous_pronouns:
    #         for token in doc:
    #             if token != ambiguous_pronoun \
    #                     and token.head == ambiguous_pronoun.head \
    #                     and (token.pos_ == 'NOUN' or token.pos_ == 'PROPN' or token.pos_ == 'VERB'):
    #                 description = token
    #                 results.append((ambiguous_pronoun, description))
    #     return results

    def getPronounDescription(self, pronoun: Token, doc: Doc) -> Optional[Token]:
        """
        For a pronoun, we define its "description token" to mean the token that
        (1) is a noun (including proper noun), a verb, or an adjective
        (2) shares the same head with the pronoun
        """
        for token in doc:
            if (token != pronoun  # description token can't be pronoun itself
                    and token.head == pronoun.head  # shares the same head with pronoun
                    and (token.pos_ == 'NOUN'  # could be a noun...
                         or token.pos_ == 'PROPN'  # ...including proper noun
                         or token.pos_ == 'VERB'  # could be a verb
                         or token.pos_ == 'ADJ')):  # could be an adjective
                return token
        return None

    def getCandidateCorefs(self, doc: Doc) -> [List[Token]]:
        """
        Candidates are simply all the nouns that are also syntactic roots,
        e.g., "apple" in "a red apple" or "subways" in "New York City subways"
        """
        return [
            token for token in doc
            if (token.pos_ == 'PROPN' or token.pos_ == 'NOUN') and token.dep_ != 'compound'
        ]

    def getCorefResolutions(
            self,
            doc: Doc,
            use_conceptnet: bool = False,
            use_retrogan_drd: bool = False
    ) -> Optional[Dict[str, Dict[Token, Token]]]:
        """
        Plural "resolutions" because there could be more than one ambiguities, i.e.,
        PatchComm has the ability to resolve multiple pronoun coreference ambiguities
        """
        def _getBestCoref(queryer, resolutions: Dict[Token, Token]) -> Dict[Token, Token]:
            # TODO & FIXME (Yida Xin, 16-Feb-2022)
            #   Instead of doing ConceptNet first and NeuralCoref next, we need to do NeuralCoref first
            #   and then ConceptNet, and then see if ConceptNet's result is different from NeuralCoref's.
            #   If so, we opt for ConceptNet's.
            for pronoun in pronouns:
                description: Optional[Token] = self.getPronounDescription(pronoun=pronoun, doc=doc)
                print(f'description == {description} for pronoun == {pronoun}')
                ## If there is no description token and NeuralCoref also doesn't have any resolution,
                ## we are screwed.
                if description is None:
                    try:
                        resolutions[pronoun] = neuralcoref_resolutions[pronoun]
                    except KeyError:  # KeyError happens when NeuralCoref doesn't have this coref
                        continue
                ## Otherwise, we try to work with the description token.
                else:
                    best_token: Optional[Token] = None
                    best_weight: float = -100.0
                    # word1: str = description.text
                    word1: str = description.lemma_  # trying out lemma instead text  - Yida Xin, 11 Nov 2021
                    for x in candidate_corefs:
                        # word2: str = x.text
                        word2: str = x.lemma_  # trying out lemma instead text  - Yida Xin, 11 Nov 2021
                        assertion: Optional[Dict[str, Any]] = queryer.getBestRelation(word1=word1, word2=word2)
                        if assertion is not None:
                            weight = assertion['weight']
                            if best_weight < weight:
                                best_weight = weight
                                best_token = x
                        else:
                            try:
                                best_token = neuralcoref_resolutions[pronoun]
                            except KeyError:
                                continue
                    resolutions[pronoun] = best_token
            return resolutions
        ## Get coref resolutions by NeuralCoref
        neuralcoref_pronouns: List[Token] = sorted(self.getNeuralcorefPronouns(doc=doc), key=lambda x: x.i)
        print(f'neuralcoref_pronouns = {[(x, x.i) for x in neuralcoref_pronouns]}\n')
        neuralcoref_resolutions: Dict[Token, Token] = self.getNeuralcorefResolutions(doc=doc)
        ## Try to get coref resolutions by ConceptNet and/or RetroGAN-DRD;
        ## if that's not possible, then default to NeuralCoref's resolutions
        pronouns: List[Token] = sorted(set(self.getPronouns(doc=doc) + neuralcoref_pronouns), key=lambda x: x.i)
        print(f'combined pronouns = {[(x, x.i) for x in pronouns]}\n')
        candidate_corefs: Optional[List[Token]] = self.getCandidateCorefs(doc=doc)
        if not pronouns or not candidate_corefs:
            return None
        conceptnet_resolutions: Dict[Token, Optional[Token]] = {}
        if use_conceptnet is True:
            conceptnet_resolutions: Dict[Token, Token] = _getBestCoref(
                queryer=self.conceptnet_queryer,
                # resolutions=conceptnet_resolutions
            )
        retrogan_drd_resolutions: Dict[Token, Optional[Token]] = {}
        if use_retrogan_drd is True:
            retrogan_drd_resolutions: Dict[Token, Token] = _getBestCoref(
                queryer=self.retrogan_drd_queryer,
                # resolutions=retrogan_drd_resolutions
            )
        ## The only reason that the returned value looks like so ridiculous is because of evaluations
        return {
            'NeuralCoref resolutions': neuralcoref_resolutions,
            'ConceptNet resolutions': conceptnet_resolutions,
            'RetroGAN-DRD resolutions': retrogan_drd_resolutions
        }
        # if (not ambiguous_pronouns_descriptions) or (not candidate_corefs):
        #     return None
        # for pair in ambiguous_pronouns_descriptions:
        #     description: Token = pair[1]
        #     if use_conceptnet is True:
        #         conceptnet_decisions[pair] = _getBestCoref(queryer=self.conceptnet_queryer)
        #     if use_retrogan_drd is True:
        #         retrogan_drd_decisions[pair] = _getBestCoref(queryer=self.retrogan_drd_queryer)
        # return {
        #     'ConceptNet resolutions': conceptnet_decisions,
        #     'RetroGAN-DRD resolutions': retrogan_drd_decisions
        # }
