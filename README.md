##### This project generates movie recommendations based off of user input of preferred movies and compares them across various features such as Genre, Duration, IMDb and MetaCritic Ratings, and year of release to get a preference of users tastes and recommend similar movies. 

##### The dataset of IMDb is taken from https://www.kaggle.com/datasets/parthdande/imdb-dataset-2024-updated/data. It is upto date data as of July, 2024 and contains more than 4000 entries in total.

### Process:
1. The datafiles are combined into one file using similarity of column names across all files
2. Preprocessing is then done on the data. Missing or duplicate values are removed. Genre titles are converted to values (e.g: action=1, animation=2). The data is then normalized between values of 0 and 1 for ease of calculation and that data corresponds to one another when finding similarities.
3. An optional file for data analysis and visualization is given to help better understand the data if it helps the creator.
![Output](https://github.com/I-Zaifa/MovieRecommendation4000/blob/main/Visualized_Data.jpg) <sub> You can tell whether the IMDb scores align with Metacritic scores based off the ball size. Which genres are the most popular (such as action and family) and what duration lengths most movies fall into (could be used to predict if a user prefers short or long movies or if this preference does not matter). </sub>
5. The processed file is saved with all the new values and the model is based off it. I used _cosine similarity_ for my similarity matching across various features of all the movies based on user input. User Input is processed with _fuzzywuzzy_ library to account for any corrections in case sensitivity or misspelling by the user. Movies with low scores are ignored.
6. Using Tkinter I wrote a basic interactive window where a user can add movies and get recommendations and be saved from the powershell.
![tkinter output](https://github.com/I-Zaifa/MovieRecommendation4000/blob/main/Tkinter%20output.jpg)

### Thoughts:
I would like to increase this projects scope in the future by having box office numbers and user reviews along with the number of votes which would allow for nlp sentiment analysis and also to judge the popularity of the movie which I currently cant. It will also help to discard irrelevant movies with very low votes even below the minimum average. 
##### The cosine similarity metric was very limited in its use here and I would like to work with a different model, which would assign proper weights to the features, If I decide to expand this project.
