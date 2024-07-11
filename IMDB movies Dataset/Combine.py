import pandas as pd

# Combines files from all common columns in all three files

file1 = 'IMDb_Dataset.csv'
file2 = 'IMDb_Dataset_2.csv'
file3 = 'IMDb_Dataset_3.csv'

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
df3 = pd.read_csv(file3)

common_columns = list(set(df1.columns) & set(df2.columns) & set(df3.columns))

df1_filtered = df1[common_columns]
df2_filtered = df2[common_columns]
df3_filtered = df3[common_columns]


combined_df = pd.concat([df1_filtered, df2_filtered, df3_filtered], ignore_index=True)


combined_df.to_csv('IMDb_combined_dataset.csv', index=False)

print("Done")

