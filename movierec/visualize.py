from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

# working with the processed data file
DATASET_PATH = Path(__file__).resolve().parent.parent / "Processed_Dataset.csv"
dataset = pd.read_csv(DATASET_PATH)

# Using imdb raitngs and duration to compare them agains each other for all the genres.
# Metascore ratings are sued to magnify the imdb ratings ball size if they align together.
plt.figure(figsize=(10, 8))
scatterplot = sn.scatterplot(
    x='IMDb Rating',
    y='Duration (minutes)',
    hue='Genre',
    size='MetaScore',  
    sizes=(20, 200),   
    palette='Set1',
    data=dataset,
    legend='brief'    
)

plt.title('IMDb Ratings vs Duration (Coloured by Genre, Ball Size by MetaScore)')
plt.xlabel('IMDb Ratings (Normalized)')
plt.ylabel('Duration (Normalized)')
plt.legend()
plt.savefig('Visualized_Data.jpg', dpi=300)  # save figure


if __name__ == "__main__":
    plt.show()  # display plot when executed directly


# This can be used to understand some basics about the data
# and set the direction you want to go in.
# It is customizable you you can see various ascepts of the data against each other.



