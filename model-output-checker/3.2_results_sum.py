# Code to sum up 1s

import pandas as pd

model_name = "llama3.1"

# Read the CSV file
df = pd.read_csv(model_name + '_checks_merged.csv')

# Group by Puzzle_ID and calculate sum for Is_Correct
results = df.groupby('Puzzle_ID').agg({
    'Is_Correct': 'sum'
}).reset_index()

# Write the results to an output CSV file
results.to_csv(model_name + '_results.csv', index=False)

print("Output file generated successfully.")
