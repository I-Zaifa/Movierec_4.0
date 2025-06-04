"""Utility for retrieving movie recommendations."""

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


def get_recommendations(user_movies_list, top_n=30):
    """Return up to ``top_n`` recommended movie titles.

    Parameters
    ----------
    user_movies_list : list[str]
        Raw user input movie titles.
    top_n : int, optional
        Maximum number of recommendations, by default ``30``.

    Returns
    -------
    list[str]
        Recommended movie titles sorted by similarity.
    """

    df = pd.read_csv("Processed_Dataset.csv")

    # Correct user movie titles using fuzzy matching
    corrected_user_movies_list = []
    for movie in user_movies_list:
        match = process.extractOne(movie.lower(), df["Title"].str.lower())
        if match and match[1] >= 70:
            corrected_user_movies_list.append(df.iloc[match[2]]["Title"])

    corrected_user_movies_list = list(set(corrected_user_movies_list))

    # Scale entire feature matrix once for consistency
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[FEATURE_COLUMNS])

    recommended_movies = []

    for movie in corrected_user_movies_list:
        movie_index = df.index[df["Title"] == movie][0]

        similarities = cosine_similarity(
            scaled_features[[movie_index]], scaled_features
        )[0]
        sorted_indices = similarities.argsort()[::-1]

        for idx in sorted_indices:
            if idx == movie_index:
                continue
            if all(
                df.iloc[idx][feature] >= 0.4 if feature != "Genre Value" else True
                for feature in FEATURE_COLUMNS
            ):
                title = df.iloc[idx]["Title"]
                if title not in corrected_user_movies_list and title not in recommended_movies:
                    recommended_movies.append(title)
                    if len(recommended_movies) >= top_n:
                        break
        if len(recommended_movies) >= top_n:
            break

    return recommended_movies


# ## usage with a random list of action movies movies
# user_liked_movies = [
#     "The Last Samurai",
#     "Rambo",
#     "Braveheart",
#     "300",
#     "Taken",
#     "The Equalizer",
#     "Casino Royale",
#     "Commando",
#     "The Rock",
#     "Bad Boys",
#     "Rush Hour",
#     "Speed",
#     "Indiana Jones and the Raiders of the Lost Ark",
#     "True Lies",
#     "The Fugitive",
#     "Point Break",
#     "Heat",
#     "Face/Off",
#     "Atomic Blonde",
#     "The Fifth Element",
#     "Hard Boiled",
#     "Kick-Ass",
#     "Man on Fire",
#     "Ip Man",
#     "The Magnificent Seven",
#     "Black Panther",
#     "Jurassic Park",
#     "The Last Samurai",
#     "Die Hard",
#     "Mad Max: Fury Road",
#     "The Dark Knight",
#     "Terminator 2: Judgment Day",
#     "Gladiator",
#     "Aliens",
#     "John Wick",
#     "The Avengers",
#     "Inception",
#     "The Matrix",
#     "Lethal Weapon",
#     "Kill Bill: Vol. 1",
#     "Braveheart",
#     "Speed",
#     "The Bourne Identity",
#     "Mad Max 2: The Road Warrior",
#     "Die Hard with a Vengeance",
#     "Predator",
#     "Commando",
#     "Indiana Jones and the Raiders of the Lost Ark",
#     "The Terminator",
#     "Mission: Impossible - Fallout",
#     "The Rock",
#     "Bad Boys",
#     "Rambo: First Blood Part II",
#     "True Lies",
#     "The Fugitive",
#     "Rush Hour",
#     "Taken",
#     "Point Break",
#     "Crouching Tiger, Hidden Dragon",
#     "Heat",
#     "Face/Off",
#     "The Equalizer",
#     "The Raid: Redemption",
#     "Atomic Blonde",
#     "The Fifth Element",
#     "Hard Boiled",
#     "Kick-Ass",
#     "Man on Fire",
#     "Casino Royale",
#     "Ip Man",
#     "John Wick: Chapter 2",
#     "The Dark Knight Rises",
# ]


# recommended_movies = get_recommendations(user_liked_movies)
# for movie in recommended_movies:
#     print(movie)
