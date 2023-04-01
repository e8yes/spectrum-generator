import emoji
import re
from nltk import word_tokenize
from typing import List

HTTP_LINK = re.compile(r"(?:\@|http?\://|https?\://|www)\S+")
OTHER_LINK = re.compile(
    r'\s*\b(?:https?:\/\/)?(?:www\.)?\S+\.(com|org|gov|ca|edu)\S*\b')
SHORT_LINK = re.compile(r'\S*\.[a-z][a-z]\/\S*')


def CleanText(text: str) -> str:
    """_summary_

    Args:
        text (str): _description_

    Returns:
        str: _description_
    """
    if text is None:
        return str()

    temp = emoji.replace_emoji(text, replace="")
    temp = temp.replace("#", "~")
    temp = temp.replace("@", "~")
    temp = temp.replace("…", "...")
    temp = temp.lower()
    temp = HTTP_LINK.sub("", temp)
    temp = OTHER_LINK.sub('', temp)
    temp = SHORT_LINK.sub('', temp)

    return temp


def TokenizeText(text: str) -> List[str]:
    """_summary_

    Args:
        text (str): _description_

    Returns:
        List[str]: _description_
    """
    words = word_tokenize(text)
    return [word for word in words if len(word) > 0]
