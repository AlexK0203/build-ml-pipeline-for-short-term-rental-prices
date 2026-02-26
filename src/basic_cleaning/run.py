#!/usr/bin/env python
"""
[An example of a step using MLflow and W&B]: Performs basic cleaning on the data and saves the results in W&B
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    df = df[df["price"].between(args.min_price, args.max_price)]
    logger.info(f"Removed rows where price was not between {args.min_price} and {args.max_price}")

    df.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This step cleans data")


    parser.add_argument(
        "--input_artifact", 
        type= str,
        help= "artifact from previous step in W&B",
        required=True
    )


    parser.add_argument(
        "--output_artifact", 
        type= str,
        help= "Name of the cleaned data set to upload",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type= str,
        help= "Type of the output",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type= str,
        help= "Description of the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type= int,
        help= "minimum price",
    )

    parser.add_argument(
        "--max_price", 
        type= int,
        help= "maximum price",
        required=True
    )

    args = parser.parse_args()

    go(args)
