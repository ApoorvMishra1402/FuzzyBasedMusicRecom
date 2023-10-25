import pandas as pd

# Load the CSV data
csv_file = 'music_genre.csv'  # Replace with your CSV file path
data = pd.read_csv(csv_file)

df = data.__dataframe__
df.style
# Drop rows with null or empty values in 'song name' and 'genre' columns
data_cleaned = data.dropna(subset=['song name', 'genre'])


# cleaned_csv_file = 'cleaned_data.csv'
# data_cleaned.to_csv(cleaned_csv_file, index=False)

print("Data cleaning and saving complete.")
