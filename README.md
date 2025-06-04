# Movie Recommendation Demo

This project generates movie suggestions based on a list of titles provided by a user. Movies are compared across genre, duration, IMDb and Metacritic ratings and year of release. The underlying dataset is sourced from [Kaggle](https://www.kaggle.com/datasets/parthdande/imdb-dataset-2024-updated/data) (July&nbsp;2024 snapshot) and contains over 4&nbsp;000 movies.

### Process:
1. Multiple raw CSV files are merged into a single dataset.
2. Preprocessing removes duplicates and missing values, maps genre names to numeric values and normalizes numerical columns.
3. ``Data_analysis_and_visualization.py`` can be used to explore the processed data.
![Output](https://github.com/I-Zaifa/MovieRecommendation4000/blob/main/Visualized_Data.jpg) <sub> You can tell whether the IMDb scores align with Metacritic scores based off the ball size. Which genres are the most popular (such as action and family) and what duration lengths most movies fall into (could be used to predict if a user prefers short or long movies or if this preference does not matter). </sub>
5. Cosine similarity is used to match the user's liked movies to other titles. Input titles are corrected with ``fuzzywuzzy`` to handle case differences or minor typos.
6. ``Main.py`` launches a small Tkinter GUI for adding movies and viewing recommendations.
![tkinter output](https://github.com/I-Zaifa/MovieRecommendation4000/blob/main/Tkinter%20output.jpg)

### Running the demo

1. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Ensure ``Processed_Dataset.csv`` exists (run ``preprocessing.py`` if necessary).
3. Execute ``python Main.py`` to launch the GUI.

### Thoughts

Future work could incorporate box‑office numbers and user reviews to help weight movie popularity. The cosine similarity approach is intentionally simple and could be replaced by a more sophisticated model in the future.
