from os import path
from torch.optim import Optimizer

from src.model.example.epoch import DataEpoch
from src.model.module.model_provider import ModelProviderInterface


def _CreateReportFile(log_path: str, model_name: str, epoch_number: int):
    report_file = path.join(
        log_path, f"{model_name}_{epoch_number}_loss")
    open(file=report_file, mode="w")


def _AppendReportFile(log_path: str,
                      model_name: str,
                      epoch_number: int,
                      progress: int,
                      loss: float):
    report_file = path.join(
        log_path, f"{model_name}_{epoch_number}_loss")

    with open(file=report_file, mode="a") as f:
        f.write(f"{progress}%,{loss}\n")


def TrainEpoch(epoch_number: str,
               model_provider: ModelProviderInterface,
               optimizer: Optimizer,
               user_tweet_file_path: str,
               log_path: str) -> None:
    """_summary_

    Args:
        epoch_number (str): _description_
        model_provider (ModelProviderInterface): _description_
        model (Module): _description_
        optimizer (Optimizer): _description_
        user_tweet_file_path (str): _description_
        log_path (str): _description_
    """
    _CreateReportFile(log_path=log_path,
                      model_name=model_provider.Name(),
                      epoch_number=epoch_number)

    epoch = DataEpoch(user_tweet_file_path=user_tweet_file_path, batch_size=64)
    model_provider.SetMode(mode="train")

    last_progress = -1
    for progress, batch in epoch:
        optimizer.zero_grad()

        loss = model_provider.Loss(user_ids=batch.user_ids,
                                   years=None,
                                   tokens=batch.masked_token_ids,
                                   attention_masks=batch.attention_masks,
                                   labels=batch.label_token_ids)
        loss.backward()

        optimizer.step()

        if progress > last_progress:
            last_progress = progress

            _AppendReportFile(
                log_path=log_path,
                model_name=model_provider.Name(),
                epoch_number=epoch_number,
                progress=progress,
                loss=loss)
