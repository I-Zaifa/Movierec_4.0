import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process

# Function that gets recommendations and is imported in another file for use
def get_recommendations(user_movies_list, top_n=30):
    df_cleaned = pd.read_csv('Processed_Dataset.csv')
    df = df_cleaned
    features = [ 'MetaScore','Duration (minutes)', 'IMDb Rating', 'Year', 'Genre Value']

    # Correct user movies list using fuzzy matching for case insensitivity or misspelling
    corrected_user_movies_list = []
    for movie in user_movies_list:
        match = process.extractOne(movie.lower(), df.iloc[:, 0].str.lower())
        if match[1] >= 70: # Similarity between input and dataset tile is 70% atleast
            corrected_user_movies_list.append(df.iloc[match[2], 0])  # Get the actual title from the DataFrame
    
    # Get unique corrected movie titles
    corrected_user_movies_list = list(set(corrected_user_movies_list))

    # Take user movies from the dataframe to get thier features
    user_movies = df[df.iloc[:, 0].isin(corrected_user_movies_list)]
    user_movie_features = user_movies[features]

    scaler = StandardScaler()
    user_movie_features_scaled = scaler.fit_transform(user_movie_features)

    # Take all movies except those in user's list for recommendation
    all_movies = df[~df.iloc[:, 0].isin(corrected_user_movies_list)]
    all_movie_features = all_movies[features]
    all_movie_features_scaled = scaler.transform(all_movie_features)

    # Calculate similarity using Cosine Similarity
    similarity_matrix = cosine_similarity(all_movie_features_scaled)

    # Sort similar movies in descending order
    similar_movies_indices = similarity_matrix.argsort(axis=1)[:, ::-1]

    # Top movies added to a list
    recommended_movies = []
    for movie in corrected_user_movies_list:
        movie_index = df[df.iloc[:, 0] == movie].index[0]
        
        for index in similar_movies_indices[movie_index]:
            # Check if all features (except genre) are above 0.4 to avoid bad films
            if all(
                (all_movie_features.iloc[index][feature] >= 0.4)
                if feature != 'Genre Value' else True  # Skip the genre value feature as 
                for feature in features
            ):
                recommended_movie_title = df.iloc[index, 0]
                if (recommended_movie_title not in corrected_user_movies_list and
                        recommended_movie_title not in recommended_movies):
                    recommended_movies.append(recommended_movie_title)
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
