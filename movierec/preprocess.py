from pathlib import Path
import argparse

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


DEFAULT_DATASET_PATH = Path(__file__).resolve().parent.parent / "IMDb_combined_dataset.csv"


def preprocess(dataset_path: Path = DEFAULT_DATASET_PATH, output_path: Path | None = None) -> Path:
    dataset = pd.read_csv(dataset_path)

    df_cleaned = dataset.drop_duplicates(subset=["Title"])
    df_cleaned = df_cleaned.dropna()

    unique_genres = df_cleaned["Genre"].unique()
    genre_mapping = {genre: idx + 1 for idx, genre in enumerate(unique_genres)}
    df_cleaned["Genre Value"] = df_cleaned["Genre"].map(genre_mapping)

    numerical_columns = [
        "MetaScore",
        "Duration (minutes)",
        "IMDb Rating",
        "Year",
        "Genre Value",
    ]
    scaler = MinMaxScaler()
    df_cleaned[numerical_columns] = scaler.fit_transform(df_cleaned[numerical_columns])

    if output_path is None:
        output_path = Path(__file__).resolve().parent.parent / "Processed_Dataset.csv"

    df_cleaned.to_csv(output_path, index=False)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Create processed movie dataset")
    parser.add_argument("--input", type=Path, default=DEFAULT_DATASET_PATH, help="Raw combined CSV file")
    parser.add_argument("--output", type=Path, default=None, help="Where to write the processed CSV")
    args = parser.parse_args()

    out_path = preprocess(args.input, args.output)
    print(f"Processed dataset written to {out_path}")


if __name__ == "__main__":
    main()
