import unittest

from src.model.example.constants import MASK_TOKEN
from src.model.example.generate_mask import SampleMaskedSentence


class GenerateMaskTest(unittest.TestCase):
    def test_SampleMaskedSentence(self):
        sentence = ["A", "A", "B"]
        word_importance = [0.0, 1.0, 0.0]

        result = SampleMaskedSentence(
            sentence=sentence, word_importance=word_importance)

        self.assertEqual(3, len(result))
        self.assertEqual("A", result[0])
        self.assertEqual(MASK_TOKEN, result[1])
        self.assertEqual("B", result[2])


if __name__ == "__main__":
    unittest.main()
