from typing import List
from typing import Dict
from math import ceil
import numpy as np

def SampleMaskedPositions(tweet_words: List[str], 
                          idf_lookup: Dict[str, float]) -> List[int]:
    idf_sum = sum(idf_lookup[word] for word in tweet_words)
    pmf = [idf_lookup[word] / idf_sum for word in tweet_words]
    mask_ratio = 0.15

    mask_index = np.random.choice(np.arange(start = 0, stop = len(tweet_words)), ceil(len(tweet_words) * mask_ratio), p = pmf)

    return mask_index