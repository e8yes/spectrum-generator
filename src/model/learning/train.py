from torch.optim import Adam

from src.dataprep.cooked.creation_year_lookup import LoadYearIdLookup
from src.dataprep.cooked.user_lookup import LoadUserLookup
from src.model.module.model_provider_factory import CreateModelProvider
from src.model.learning.epoch import TrainEpoch


def _DetermineYearCount(input_path: str) -> int:
    lookup = LoadYearIdLookup(input_path=input_path)
    return len(lookup)


def _DetermineUserCount(input_path: str) -> int:
    lookup = LoadUserLookup(input_path=input_path)
    return len(lookup)


def TrainModel(model_type: str,
               existing_model_path: str,
               epoch_count: int,
               input_path: str,
               output_path: str) -> None:
    """_summary_

    Args:
        model_type (str): _description_
        existing_model_path (str): _description_
        epoch_count (int): _description_
        input_path (str): _description_
        output_path (str): _description_

    Returns:
        _type_: _description_
    """
    user_count = _DetermineUserCount(input_path=input_path)
    year_count = _DetermineYearCount(input_path=input_path)
    model_provider = CreateModelProvider(model_type=model_type,
                                         user_count=user_count,
                                         year_count=year_count)
    model_provider.LoadOrCreate(model_path=existing_model_path)

    params, param_count = model_provider.TrainableParameters()
    optimizer = Adam(params=params)

    print(f"model={model_provider.Name()} param_count={param_count}")

    for epoch_num in range(epoch_count):
        print(f"model={model_provider.Name()} @{epoch_num}")
        model_provider.Save(
            model_path=output_path, tag=str(epoch_num))
        model_provider.ExportExtractedInsights(
            output_path=output_path, tag=str(epoch_num))

        TrainEpoch(epoch_number=epoch_num,
                   model_provider=model_provider,
                   optimizer=optimizer,
                   input_path=input_path,
                   log_path=output_path)

    model_provider.Save(
        model_path=output_path, tag="final")
    model_provider.ExportExtractedInsights(
        output_path=output_path, tag="final")

    print(f"model={model_provider.Name()} finished.")
