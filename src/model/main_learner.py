import argparse

from src.model.learning.train import TrainModel


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train a model over the user tweet data.")

    parser.add_argument(
        "--user_lookup_file",
        type=str,
        help="Path to the user lookup JSON file.")
    parser.add_argument(
        "--user_tweets_file",
        type=str,
        help="Path to the user tweets dataframe file.")
    parser.add_argument(
        "--model_type", type=str,
        help="The type of model to train for. Values can either be baseline or"
        " personalized")
    parser.add_argument(
        "--epoch_count", type=int,
        help="The number of epochs to train for.")
    parser.add_argument(
        "--existing_model_file", type=str,
        help="Optional. Path to an existing model. Supplying this argument"
        " allows the program to continue training from the existing state.")
    parser.add_argument(
        "--output_path",
        type=str,
        help="Path under which the trained models and logs are stored.")

    args = parser.parse_args()

    if args.user_lookup_file is None:
        print("user_lookup_file is required.")
        exit(-1)
    if args.user_tweets_file is None:
        print("user_tweets_file is required.")
        exit(-1)
    if args.model_type is None:
        print("model_type is required.")
        exit(-1)
    if args.epoch_count is None:
        print("epoch_count is required.")
        exit(-1)
    if args.output_path is None:
        print("output_path is required.")
        exit(-1)

    TrainModel(model_type=args.model_type,
               existing_model_path=args.existing_model_file,
               epoch_count=args.epoch_count,
               user_tweet_file_path=args.user_tweets_file,
               user_lookup_file_path=args.user_lookup_file,
               output_path=args.output_path)
