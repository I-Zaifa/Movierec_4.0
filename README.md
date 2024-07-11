##### This project generates movie recommendations based off of user input of preferred movies and compares them across various features such as Genre, Duraion, IMDb and MetaCritic Ratings, and year of release to get a prefernce of users tastes and recommend similar movies. 

##### The dataset of imdb is taken from https://www.kaggle.com/datasets/parthdande/imdb-dataset-2024-updated/data. It is upto date data as of July, 2024 and contains more than 4000 entries in total.

### Process:
1. The datafiles are combined into one file using similarity of column names accross all files
2. Preprocessing is then done on the data. Missing or duplicate values are removed. Genre titles are converted to values (e.g: action=1, animation=2). The data is then normalized between values of 0 and 1 for ease of calculation and that data correesponds to one another when finding similarities.
3. An optional file for data analysis and visualization is given to help better understand the data if it helps the creator.
![Output](https://github.com/I-Zaifa/MovieRecommendation4000/blob/main/Visualized_Data.jpg) <sub> You can tell whether the imdb scores align with metacritic scroes based off the ball size. WHich genres are the most popular (such as action and family) and what duration lenghts most movies fall into (could be used to predict if a user prefers short or long movies or if the preferance does not matter). </sub>
5. 
