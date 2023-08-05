import unittest
from src.patchcomm.models.sentence_parser import SentenceParser
# from patchcomm.models.coref_resolver import CoreferenceResolver
from src.patchcomm.visualizer.dependency_parse_visualizer import DependencyParseVisualizer


class TestVisualizer(unittest.TestCase):
    def setUp(self) -> None:
        # print('')
        # self.sentence = str(input('Type a sentence: '))
        self.sentence_parser = SentenceParser()
        # self.sentence_parser = CoreferenceResolver(sentence)
        # self.doc = self.sentence_parser.doc
        self.dependency_parse_visualizer = DependencyParseVisualizer(
            sentence_parser=self.sentence_parser
        )
        # print('')

    def test_dependency_parse_visualizer(self):
        while True:
            try:
                print('')
                sentence = str(input('Type a sentence: '))
                print('')
                self.dependency_parse_visualizer.serve(sentence=sentence)
            except KeyboardInterrupt:
                break


if __name__ == '__main__':
    unittest.main()
