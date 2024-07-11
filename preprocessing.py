import pandas as pd 
import numpy as np 
from sklearn.preprocessing import MinMaxScaler


dataset = pd.read_csv('IMDb_combined_dataset.csv')


### Removing missing (some columns not having data) or duplicate values ###
df_cleaned = dataset.drop_duplicates(subset=['Title'])
removed_duplicates = dataset[dataset.duplicated(subset=['Title'], keep=False)]
# print(removed_duplicates)

missing_values = df_cleaned.isnull().any(axis=1)
removed_rows = df_cleaned[missing_values]
df_cleaned = df_cleaned.dropna()
# print(removed_rows) # None here actually but just in case for future updates

### Converting Genres to Numbers
unique_genres = df_cleaned['Genre'].unique()
genre_mapping = {genre: idx + 1 for idx, genre in enumerate(unique_genres)}
df_cleaned['Genre Value'] = df_cleaned['Genre'].map(genre_mapping)
print(df_cleaned["Genre Value"])

### Normalizing the data (b/w 0 and 1) ###

numerical_columns = ['MetaScore', 'Duration (minutes)', 'IMDb Rating', 'Year', 'Genre Value']
scaler = MinMaxScaler()

df_cleaned[numerical_columns] = scaler.fit_transform(df_cleaned[numerical_columns])
# df_cleaned[numerical_columns] = df_cleaned[numerical_columns].round(2)
# print(df_cleaned['Duration (minutes)'])


### Save to a new file ###
df_cleaned.to_csv("Processed_Dataset.csv", index=False)