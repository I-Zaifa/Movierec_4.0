"""High level recommendation utilities."""

from pathlib import Path
from typing import Iterable, List, Mapping

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances
from fuzzywuzzy import process


FEATURE_COLUMNS = [
    "MetaScore",
    "Duration (minutes)",
    "IMDb Rating",
    "Year",
    "Genre Value",
]

# Default feature weights used for weighted similarity scoring.
DEFAULT_FEATURE_WEIGHTS = {
    "MetaScore": 0.8,
    "Duration (minutes)": 0.3,
    "IMDb Rating": 1.2,
    "Year": 0.5,
    "Genre Value": 0.5,
}


class MovieRecommender:
    """Provide movie recommendations based on liked titles."""

    def __init__(
        self,
        dataset_path: Path | None = None,
        feature_weights: Mapping[str, float] | None = None,
    ) -> None:
        self.dataset_path = (
            Path(dataset_path)
            if dataset_path is not None
            else Path(__file__).resolve().parent.parent / "Processed_Dataset.csv"
        )
        self._df = pd.read_csv(self.dataset_path)
        self._df["Title"] = self._df["Title"].astype(str)
        scaler = StandardScaler()
        scaled = scaler.fit_transform(self._df[FEATURE_COLUMNS])

        weights = [
            (feature_weights or DEFAULT_FEATURE_WEIGHTS).get(col, 1.0)
            for col in FEATURE_COLUMNS
        ]
        self._weights = pd.Series(weights, index=FEATURE_COLUMNS)
        self._scaled_features = scaled * self._weights.values

    def _correct_titles(self, titles: Iterable[str]) -> list[str]:
        fixed = []
        for movie in titles:
            match = process.extractOne(movie.lower(), self._df["Title"].str.lower())
            if match and match[1] >= 70:
                fixed.append(self._df.iloc[match[2]]["Title"])
        return list(set(fixed))

    def recommend(self, liked_titles: Iterable[str], top_n: int = 30) -> List[str]:
        """Return up to ``top_n`` recommended movie titles."""

        corrected = self._correct_titles(liked_titles)
        if not corrected:
            return []

        indices = [self._df.index[self._df["Title"] == title][0] for title in corrected]
        user_vector = self._scaled_features[indices].mean(axis=0, keepdims=True)

        # Using cosine distance on weighted, standardised features tends to
        # surface more nuanced similarities than plain Euclidean distance.
        distances = pairwise_distances(
            user_vector, self._scaled_features, metric="cosine"
        )[0]
        sorted_indices = distances.argsort()

        recommended: list[str] = []
        for idx in sorted_indices:
            if idx in indices:
                continue
            if all(
                self._df.iloc[idx][feature] >= 0.4 if feature != "Genre Value" else True
                for feature in FEATURE_COLUMNS
            ):
                title = self._df.iloc[idx]["Title"]
                if title not in recommended:
                    recommended.append(title)
                    if len(recommended) >= top_n:
                        break

        return recommended


def get_recommendations(
    user_movies_list: Iterable[str],
    top_n: int = 30,
    *,
    feature_weights: Mapping[str, float] | None = None,
) -> List[str]:
    """Backwards compatible wrapper around :class:`MovieRecommender`."""

    return MovieRecommender(feature_weights=feature_weights).recommend(
        user_movies_list, top_n=top_n
    )
