# Best model vs Humans -- avg in latex table: overall + conditions
# Additionally, removing 'nan' from csv description

import pandas as pd
import numpy as np

# Constants for normalization
MODEL_MAX_SCORE = 5.0
HUMAN_MAX_SCORE = 5.0


# Read CSV files and convert 'Is_Correct' to numeric
def read_and_prepare(filename, max_score):
    df = pd.read_csv(filename, names=['Puzzle_ID', 'Is_Correct'])
    df['Is_Correct'] = pd.to_numeric(df['Is_Correct'], errors='coerce').dropna().astype(int)
    df['Normalized_Is_Correct'] = df['Is_Correct'] / max_score
    return df


# Perform the permutation test
def permutation_test(sample1, sample2, num_permutations=10000):
    obs_diff = np.abs(np.mean(sample1) - np.mean(sample2))
    pooled = np.hstack([sample1, sample2])
    n = len(sample1)

    count = 0
    for _ in range(num_permutations):
        np.random.shuffle(pooled)
        new_diff = np.abs(np.mean(pooled[:n]) - np.mean(pooled[n:]))
        if new_diff >= obs_diff:
            count += 1

    return count / num_permutations


# Function to format LaTeX table with normalized scores and significance
def generate_latex_table(header, data_rows, caption, label):
    latex = "\\begin{table}[h!]\n\\centering\n\\begin{tabular}{|" + "|".join(['l'] * len(header)) + "|}\n\\hline\n"
    latex += " & ".join(header) + " \\\\\n\\hline\n"
    for row in data_rows:
        row_data = [f"{cell:.2f}" if isinstance(cell, float) else str(cell) for cell in row]
        latex += " & ".join(row_data) + " \\\\\n"
    latex += "\\hline\n\\end{tabular}\n\\caption{" + caption + "}\n\\label{" + label + "}\n\\end{table}\n"
    return latex


# Main function
def main():
    # Read data and normalize scores
    model_df = read_and_prepare('results_csv/model_results.csv', MODEL_MAX_SCORE)
    human_df = read_and_prepare('results_csv/human_results_top5.csv', HUMAN_MAX_SCORE)

    # Variations, 'overall' included
    variations = ['adversarial', 'common', 'linguistic_obfuscation', 'math', 'parametrization']

    # Table 1: Generate average normalized scores for 'common' and 'overall'
    table1_variations = ['common', 'overall']
    header = ['Group'] + [var.capitalize().replace('_', ' ') for var in table1_variations]
    table1_data_rows = [
        ['Best model'],
        ['Human'],
        ['P-value']
        # ['Significance']
    ]

    for var in table1_variations:
        var_key = var if var != 'overall' else None
        model_scores = model_df[model_df['Puzzle_ID'].str.contains(var)]['Normalized_Is_Correct'] if var_key else \
        model_df['Normalized_Is_Correct']
        human_scores = human_df[human_df['Puzzle_ID'].str.contains(var)]['Normalized_Is_Correct'] if var_key else \
        human_df['Normalized_Is_Correct']

        # removing 'nan' (csv description)
        # model_scores = model_scores[~np.isnan(model_scores)]
        # human_scores = human_scores[~np.isnan(human_scores)]

        model_avg = model_scores.mean()
        human_avg = human_scores.mean()

        p_value = permutation_test(model_scores.values, human_scores.values)

        table1_data_rows[0] += [model_avg]
        table1_data_rows[1] += [human_avg]
        table1_data_rows[2] += [str(p_value) + '*' * int(p_value < 0.05)]
        # table1_data_rows[3] += ['*' if p_value < 0.05 else 'ns']

    print(generate_latex_table(header, table1_data_rows,
                               "Normalized Average Correct Scores for Common and Overall Variations",
                               "tab:common_overall"))

    # Table 2: Generate average normalized scores for all variations
    header = ['Group'] + ['Overall'] + [var.capitalize().replace('_', ' ') for var in variations]
    table2_data_rows = [
        ['Best model'],
        ['Human'],
        ['P-value']
        # ['Significance']
    ]

    for var in [None] + variations:
        var_key = var
        model_scores = model_df[model_df['Puzzle_ID'].str.contains(var_key)]['Normalized_Is_Correct'] if var_key else \
        model_df['Normalized_Is_Correct']
        human_scores = human_df[human_df['Puzzle_ID'].str.contains(var_key)]['Normalized_Is_Correct'] if var_key else \
        human_df['Normalized_Is_Correct']

        # removing 'nan' (csv description)
        # model_scores = model_scores[~np.isnan(model_scores)]
        # human_scores = human_scores[~np.isnan(human_scores)]

        model_avg = model_scores.mean()
        human_avg = human_scores.mean()

        p_value = permutation_test(model_scores.values, human_scores.values) if len(model_scores) > 0 and len(
            human_scores) > 0 else 'N/A'

        table2_data_rows[0] += [model_avg]
        table2_data_rows[1] += [human_avg]
        table2_data_rows[2] += [str(p_value) + '*' * int(p_value < 0.05)]
        # table2_data_rows[3] += ['*' if p_value < 0.05 else 'ns']

    print(generate_latex_table(header, table2_data_rows,
                               "Normalized Average Correct Scores for Each Variation and Overall",
                               "tab:all_variations"))


if __name__ == '__main__':
    main()