from typing import List, Dict, Optional, Any
from spacy.tokens import Token, Doc


class PrepositionalPhraseAttacher:
    def __init__(self, conceptnet_queryer=None, retrogan_drd_queryer=None):
        if conceptnet_queryer is not None:
            self.conceptnet_queryer = conceptnet_queryer
        if retrogan_drd_queryer is not None:
            self.retrogan_drd_queryer = retrogan_drd_queryer
        ## spaCy Prepositional Phrase Attachment
        # self.ignored_preps = ['through', 'across', 'into', 'of']
        self.accepted_preps = ['about', 'at', 'from', 'on', 'in', 'for', 'with']

    def getPPs(self, doc: Doc) -> Optional[List[List[Token]]]:
        """
        For our purposes, each prepositional phrase will simply be the preposition and the noun,
        e.g., ['with', 'fingers'] instead of ['with', 'two', 'fingers']
        """
        prep_phrases: List[List[Token]] = []
        for token in doc:
            if (token.dep_ == 'prep') and (token.text in self.accepted_preps):
                prep_idx: int = token.i
                noun_idx: int = prep_idx + 1
                while doc[noun_idx].pos_ != 'NOUN':
                    noun_idx += 1
                prep_phrases.append([doc[prep_idx], doc[noun_idx]])
        if len(prep_phrases) == 0:
            return None
        return prep_phrases

    def getPrepFromPP(self, prep_phrase: List[Token]) -> Token:
        return prep_phrase[0]

    def getModifierFromPP(self, prep_phrase: List[Token]) -> Token:
        """
        At the moment (as of 02/02/2021), there isn't any modifier in any prep-phrase in self.prepositional_phrases
        """
        pass

    def getConceptFromPP(self, prep_phrase: List[Token]) -> Token:
        return prep_phrase[1]

    def getCandidateAttachmentsForPP(self, prep_phrase: List[Token], doc: Doc) -> List[Token]:
        """
        Get, as candidate attachments, all verbs and nouns for the given prep_phrase,
        i.e., literally all the verbs and nouns that occur before this prep_phrase
        """
        prep_phrase_token = prep_phrase[-1]
        candidate_idx = 0
        candidate_attachments = []
        while candidate_idx < prep_phrase_token.i:
            if doc[candidate_idx].pos_ == 'VERB' or doc[candidate_idx].pos_ == 'NOUN':
                candidate_attachments.append(doc[candidate_idx])
            candidate_idx += 1
        return candidate_attachments

    def getAmbiguousPPAttachs(self, doc: Doc) -> Optional[Dict[Token, List[Token]]]:
        """
        Get all the ambiguous PP attachments in the sentence, could be more than one
        """
        prepositional_phrases = self.getPPs(doc=doc)
        if prepositional_phrases is not None:
            return {
                pp[-1]: self.getCandidateAttachmentsForPP(prep_phrase=pp, doc=doc)
                for pp in prepositional_phrases
            }
        return None

    def getAttachments(
            self,
            doc: Doc,
            use_conceptnet: bool = False,
            use_retrogan_drd: bool = False
    ) -> Optional[Dict[str, Dict[Token, Optional[Token]]]]:
        """
        Plural "attachments" because there could be more than one ambiguities, i.e.,
        PatchComm has the ability to resolve multiple PP attachment ambiguities
        """
        def _getBestAttachment(queryer) -> Optional[Token]:
            best_token: Optional[Token] = None
            best_weight: float = -100.0
            # word1: str = prep_phrase_token.text
            word1: str = prep_phrase_token.lemma_  # trying out lemma instead text  - Yida Xin, 11 Nov 2021
            for x in candidate_attachments:
                # word2: str = x.text
                word2: str = x.lemma_  # trying out lemma instead text  - Yida Xin, 11 Nov 2021
                assertion: Optional[Dict[str, Any]] = queryer.getBestRelation(word1=word1, word2=word2)
                if assertion is not None:
                    weight = assertion['weight']
                    if best_weight < weight:
                        best_weight = weight
                        best_token = x
            return best_token
        ## Try to get ppattach decision using ConceptNet and/or RetroGAN-DRD;
        ## if that's not possible, then default back to spaCy
        conceptnet_decisions: Dict[Token, Optional[Token]] = {}
        retrogan_drd_decisions: Dict[Token, Optional[Token]] = {}
        ambiguous_ppattachs: Dict[Token, List[Token]] = self.getAmbiguousPPAttachs(doc=doc)
        if not ambiguous_ppattachs:
            return None
        for prep_phrase_token, candidate_attachments in ambiguous_ppattachs.items():
            ## Get attachments via ConceptNet directly
            if use_conceptnet is True:
                conceptnet_decisions[prep_phrase_token] = _getBestAttachment(queryer=self.conceptnet_queryer)
            ## Get attachments via RetroGAN-DRD
            if use_retrogan_drd is True:
                retrogan_drd_decisions[prep_phrase_token] = _getBestAttachment(queryer=self.retrogan_drd_queryer)
        return {
            'ConceptNet decisions': conceptnet_decisions,
            'RetroGAN-DRD decisions': retrogan_drd_decisions
        }
