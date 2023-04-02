from src.model.module.model_provider import ModelProviderInterface
from src.model.module.model_baseline import BaselineModelProvider
from src.model.module.model_personalized import \
    PersonalizedModelProvider


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
        return BaselineModelProvider()
    elif model_type == "personalized":
        return PersonalizedModelProvider(user_count=user_count)
    else:
        assert False
