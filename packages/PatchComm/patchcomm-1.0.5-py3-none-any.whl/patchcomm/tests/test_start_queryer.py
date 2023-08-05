from __future__ import absolute_import, unicode_literals
import unittest
from src.patchcomm.models.start_queryer import StartParserQueryer


class TestStartQueryer(unittest.TestCase):
    def setUp(self) -> None:
        # sentence = str(input('\nType a sentence: '))
        # self.sentence = sentence
        self.start_parser_queryer = StartParserQueryer()

    # def testStartInitialParse(self):
    #     print(f'START initial parse:\n{self.start_parser_queryer.getStartInitialParse(self.sentence)}\n')

    def testStartTriples(self):
        # print(f'START triples:\n{self.start_parser_queryer.getStartTriples(self.sentence)}\n')
        while True:
            try:
                print('')
                sentence = str(input('Type a sentence: '))
                print('')
                for t in self.start_parser_queryer.getStartTriples(sentence):
                    print(t)
                print('')
            except KeyboardInterrupt:
                break


if __name__ == '__main__':
    unittest.main()
