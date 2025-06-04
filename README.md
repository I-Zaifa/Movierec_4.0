# Movie Recommendation Demo

This project generates movie suggestions based on a list of titles provided by a user. Movies are compared across genre, duration, IMDb and Metacritic ratings and the year of release. The underlying dataset comes from [Kaggle](https://www.kaggle.com/datasets/parthdande/imdb-dataset-2024-updated/data) (July 2024 snapshot) and contains over 4,000 movies.

## Process
1. Multiple raw CSV files are merged into a single dataset.
2. Preprocessing removes duplicates and missing values, maps genre names to numeric values and normalizes the numerical columns.
3. The optional `movierec.visualize` module can be used to explore the processed data.
   
   ![Output](https://github.com/I-Zaifa/MovieRecommendation4000/blob/main/Visualized_Data.jpg)
4. Cosine similarity matches the user's liked movies to other titles. Input titles are corrected with `fuzzywuzzy` to handle case differences or minor typos.
5. Recommendations are served by a `MovieRecommender` class that preloads and scales the dataset.
6. A GUI can be launched via `python -m movierec` or recommendations can be printed in the terminal with the `--movies` option.
   
   ![Tkinter output](https://github.com/I-Zaifa/MovieRecommendation4000/blob/main/Tkinter%20output.jpg)

## Running the demo

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Ensure `Processed_Dataset.csv` exists (run `movierec.preprocess` if necessary).
3. Launch the GUI:

```bash
python -m movierec
```

You can also request recommendations directly from the terminal:

```bash
python -m movierec --movies "The Matrix, Inception"
```

## Thoughts

Future work could incorporate box‑office numbers and user reviews to help weight movie popularity. The cosine similarity approach is intentionally simple and could be replaced by a more sophisticated model in the future.
