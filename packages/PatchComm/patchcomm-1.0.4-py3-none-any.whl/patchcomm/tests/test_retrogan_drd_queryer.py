import unittest
from src.patchcomm.models.retrogan_drd_queryer import RetroganDrdQueryer


class TestRetroganDrdQueryer(unittest.TestCase):
    def setUp(self):
        print('+-------------------------------+')
        print('| Loading embeddings and models |')
        print('+-------------------------------+')
        self.retrogan_drd_queryer = RetroganDrdQueryer()
        print('+------+')
        print('| Done |')
        print('+------+')

    def testGetBestRelation(self):
        while True:
            try:
                print('--\n')
                word1 = str(input('Type 1st word: '))
                word2 = str(input('Type 2nd word: '))
                print('')
                best_relation = self.retrogan_drd_queryer.getBestRelation(word1=word1, word2=word2)
                print(f'Best relation name: {best_relation[0]} | score: {best_relation[1]}')
                print('')
            except KeyboardInterrupt:
                break


if __name__ == '__main__':
    unittest.main()
