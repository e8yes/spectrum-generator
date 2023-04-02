from src.model.module.model_provider import ModelProviderInterface
from src.model.module.masked_lm import BaselineMaskedLanguageModelProvider
from src.model.module.profile_extractor import \
    UserProfileExtractionModelProvider


def CreateModelProvider(model_type: str,
                        user_count: int) -> ModelProviderInterface:
    """_summary_

    Args:
        model_type (str): _description_
        user_count (int): _description_

    Returns:
        ModelProviderInterface: _description_
    """
    if model_type == "baseline":
        return BaselineMaskedLanguageModelProvider()
    elif model_type == "personalized":
        return UserProfileExtractionModelProvider(user_count=user_count)
    else:
        assert False
