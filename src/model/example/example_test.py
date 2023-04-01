import unittest

from src.model.example.example import SampleSentenceMask


class ExampleTest(unittest.TestCase):
    def test_SampleSentenceMask(self):
        sentence1 = ["A", "A", "B"]
        sentence2 = ["A", "~A", "B"]
        word_importance = [0.0, 1.0, 0.0]

        result = SampleSentenceMask(
            sentence=sentence1, word_importance=word_importance)

        self.assertEqual(1, len(result))
        self.assertTrue(1 in result)

        result = SampleSentenceMask(
            sentence=sentence2, word_importance=word_importance)

        self.assertEqual(0, len(result))


if __name__ == "__main__":
    unittest.main()
