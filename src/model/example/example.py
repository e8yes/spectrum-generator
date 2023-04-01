from typing import List
from math import ceil
import numpy as np

from src.model.example.constants import MASK_TOKEN


def SampleMaskedSentence(sentence: List[str],
                         word_importance: List[float],
                         mask_ratio: float = 0.15) -> List[int]:
    """_summary_

    Args:
        sentence (List[str]): _description_
        word_importance (List[float]): _description_
        mask_ratio (float, optional): _description_. Defaults to 0.15.

    Returns:
        List[int]: _description_
    """
    word_count = len(sentence)
    mask_count = min(word_count, ceil(word_count * mask_ratio))
    positions = np.arange(start=0, stop=word_count)
    masked_positions = np.random.choice(
        a=positions, size=mask_count, p=word_importance)

    targets = set(masked_positions)
    result = list()
    for i in range(word_count):
        if i not in targets or sentence[i].startswith("~"):
            result.append(sentence[i])
        else:
            result.append(MASK_TOKEN)

    return result
