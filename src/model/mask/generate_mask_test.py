import unittest

from src.model.mask.generate_mask import SampleMaskedPositions

class GenerateMaskTest(unittest.TestCase):
    def test_SampleMaskedPositions(self):
        words = ["A", "A", "B"]
        idf_lookup = {
            "A": 0.0,
            "B": 1.0,
        }

        result = SampleMaskedPositions(tweet_words=words, idf_lookup=idf_lookup)

        self.assertEqual(1, len(result))
        self.assertEqual(2, result[0])

if __name__ == "__main__":
    unittest.main()
