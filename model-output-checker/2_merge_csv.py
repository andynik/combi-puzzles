# Code to merge several output files into one file

import pandas as pd
import os

model_name = "llama3.1"

def merge_csv_files(input_dir, output_file):
    # Get list of CSV files in the input directory
    csv_files = [file for file in os.listdir(input_dir) if file.endswith('.csv')]

    # Initialize an empty list to store DataFrames
    dfs = []

    # Iterate over each CSV file and append its data to the list
    for file in csv_files:
        file_path = os.path.join(input_dir, file)
        df = pd.read_csv(file_path)
        dfs.append(df)

    # Concatenate all DataFrames in the list
    merged_data = pd.concat(dfs, ignore_index=True)

    # Write merged data to a new CSV file
    merged_data.to_csv(output_file, index=False)
    print(f"Merged data saved to {output_file}")


# Example usage:
input_directory = model_name + '_checks'  # Specify the directory containing CSV files
output_file = model_name + '_checks_merged.csv'  # Specify the name of the output merged CSV file
merge_csv_files(input_directory, output_file)
