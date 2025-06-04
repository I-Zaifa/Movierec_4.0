"""High level recommendation utilities."""

from pathlib import Path
from typing import Iterable, List

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process


FEATURE_COLUMNS = [
    "MetaScore",
    "Duration (minutes)",
    "IMDb Rating",
    "Year",
    "Genre Value",
]


class MovieRecommender:
    """Provide movie recommendations based on liked titles."""

    def __init__(self, dataset_path: Path | None = None) -> None:
        self.dataset_path = (
            Path(dataset_path)
            if dataset_path is not None
            else Path(__file__).resolve().parent.parent / "Processed_Dataset.csv"
        )
        self._df = pd.read_csv(self.dataset_path)
        self._df["Title"] = self._df["Title"].astype(str)
        scaler = StandardScaler()
        self._scaled_features = scaler.fit_transform(self._df[FEATURE_COLUMNS])

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
        recommended: list[str] = []

        for movie in corrected:
            movie_index = self._df.index[self._df["Title"] == movie][0]

            similarities = cosine_similarity(
                self._scaled_features[[movie_index]], self._scaled_features
            )[0]
            sorted_indices = similarities.argsort()[::-1]

            for idx in sorted_indices:
                if idx == movie_index:
                    continue
                if all(
                    self._df.iloc[idx][feature] >= 0.4 if feature != "Genre Value" else True
                    for feature in FEATURE_COLUMNS
                ):
                    title = self._df.iloc[idx]["Title"]
                    if title not in corrected and title not in recommended:
                        recommended.append(title)
                        if len(recommended) >= top_n:
                            break
            if len(recommended) >= top_n:
                break

        return recommended


def get_recommendations(user_movies_list: Iterable[str], top_n: int = 30) -> List[str]:
    """Backwards compatible wrapper around :class:`MovieRecommender`."""

    return MovieRecommender().recommend(user_movies_list, top_n=top_n)

