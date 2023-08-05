import unittest
from src.patchcomm.models.start_queryer import StartParserQueryer
from src.patchcomm.models.sentence_parser import SentenceParser


class TestSentenceParser(unittest.TestCase):
    def setUp(self) -> None:
        # # print('')
        # # sentence = str(input('Type a sentence: '))
        self.start = StartParserQueryer()
        # self.sentence = 'John plays his guitar with two strings in his chair'
        # # print('')
        self.sentence_parser = SentenceParser()
        # # print('')
        # # self.sentence_parser.sentence = str(input('Type a sentence: '))
        # print('')

    # # def testOneSentence(self):
    # #     """
    # #     e.g., John plays his guitar with two fingers
    # #     e.g., John vigorously plays his cool guitar with two tough fingers
    # #     e.g., John plays his guitar with two fingers in his chair
    # #     """
    # #     # TODO
    # #     #   Add displaCy visualizer code here
    # #     print('')
    # #     print(f'self.sentence_parser.sentence == {self.sentence_parser.sentence}')
    # #     print('')
    # #     print(f'self.sentence_parser.doc == {self.sentence_parser.doc}')
    # #     print('')
    # #     # print(f'Parse:\n{self.sentence_parser.getSentenceParse()}')
    # #     print('Parse:')
    # #     print('')
    # #     for i, arc in self.sentence_parser.parse().items():
    # #         print(f'{i}: {arc}')
    # #     print('')
    #
    # def testPPAttachDecisionsViaConceptnet(self):
    #     print(f'pp-attach decisions via ConceptNet:\n{self.sentence_parser.ppattach_decisions}\n')

    def testStartParse(self):
        while True:
            try:
                print('')
                sentence = str(input('Type a sentence: '))
                print('\n==========\n')
                print('Original START parse:')
                for x in self.start.getStartTriples(sentence=sentence):
                    print(f'  {x}')
                print('')
                print('Improved START parse:')
                # self.sentence_parser.getStartParse()
                for x in self.sentence_parser.getStartParse(sentence=sentence, use_conceptnet=True, use_retrogan_drd=False):
                    print(f'  {x}')
                print('')
            except KeyboardInterrupt:
                break

    # def testSpacyParse(self):
    #     while True:
    #         try:
    #             print('')
    #             sentence = str(input('Type a sentence: '))
    #             print('\n==========\n')
    #             print('Original spaCy parse:')
    #             print(parse_deps(sentence))
    #             print('')
    #             print('Improved spaCy parse:')
    #             print(self.sentence_parser.getSpacyParse(sentence=sentence, use_conceptnet=True, use_retrogan_drd=False))
    #             print('')
    #         except KeyboardInterrupt:
    #             break


if __name__ == '__main__':
    unittest.main()
