import pandas as pd
import numpy as np


# Function to perform permutation tests
def permutation_test(sample1, sample2, num_permutations=10000):
    observed_diff = np.mean(sample1) - np.mean(sample2)
    pooled = np.concatenate([sample1, sample2])
    perm_diffs = []

    for _ in range(num_permutations):
        np.random.shuffle(pooled)
        new_diff = np.mean(pooled[:len(sample1)]) - np.mean(pooled[len(sample1):])
        perm_diffs.append(new_diff)

    p_val = np.mean(np.abs(perm_diffs) >= np.abs(observed_diff))
    return observed_diff, p_val


# Function to calculate averages and permutation tests for all condition pairs
def calculate_averages_and_differences(df, conditions, max_problems):
    # Calculate averages for each condition
    averages = {
        condition: df[df['Puzzle_ID'].str.contains(condition)]['Is_Correct'].mean() / max_problems
        for condition in conditions
    }

    num_conditions = len(conditions)
    matrix = np.zeros((num_conditions, num_conditions), dtype=object)

    for i, condition1 in enumerate(conditions):
        for j, condition2 in enumerate(conditions):
            if condition1 != condition2:
                # Use precomputed averages to calculate differences (rounded to .DD)
                diff = round(averages[condition1], 2) - round(averages[condition2], 2)
                # Perform permutation test using the original data
                group1 = df[df['Puzzle_ID'].str.contains(condition1)]['Is_Correct']
                group2 = df[df['Puzzle_ID'].str.contains(condition2)]['Is_Correct']
                _, p_val = permutation_test(group1.values / max_problems, group2.values / max_problems)
                # Store formatted diff and p-value
                matrix[i, j] = f'{diff:.2f}, {p_val:.3f}'
            else:
                matrix[i, j] = '/'

    return averages, np.tril(matrix, -1)  # Returning the lower triangular matrix


# Function to convert the results into a LaTeX table
def matrix_to_latex(averages, matrix, conditions, title):
    def format_value(val):
        """Formats values to .DD or -.DD by stripping leading zeros"""
        formatted = f"{val:+.2f}"
        return formatted.replace("+0.", ".").replace("-0.", "-.")

    latex_str = "\\begin{table*}[htbp]\\centering\\small\n"
    latex_str += "\\begin{tabular}{|l|c" + "c" * len(conditions) + "|}\n\\hline\n"
    latex_str += f"\\textbf{{{title}}} & & " + " & ".join(
        cond.replace("_", " ").capitalize() for cond in conditions) + " \\\\\n\\hline\n"

    # Average Row
    latex_str += "& & " + " & ".join(format_value(averages[cond]) for cond in conditions) + " \\\\\n\\hline\n"

    # Difference Rows
    for i, cond1 in enumerate(conditions):
        row_str = f"{cond1.replace('_', ' ').capitalize()} & {format_value(averages[cond1])} "
        for j in range(len(conditions)):
            if i == j:
                row_str += "& - "
            elif i < j:
                row_str += "& "
            else:
                diff_str, p_str = matrix[i, j].split(',')
                diff_value = format_value(float(diff_str))
                p_val = float(p_str)
                if p_val < 0.05:
                    row_str += f"& {diff_value}* ({p_val:.3f}) "
                else:
                    row_str += f"& {diff_value} "
        latex_str += row_str + "\\\\\n"

    latex_str += "\\hline\n\\end{tabular}\n"
    latex_str += f"\\caption{{Comparison between variations for {title.lower()}. Significant differences are marked with an asterisk ($p < .05$) with p-value in brackets.}}\n"
    latex_str += "\\end{table*}\n"
    return latex_str


# Read in the data
model_results_df = pd.read_csv('results_csv/model_results.csv')
human_results_df = pd.read_csv('results_csv/human_results.csv')

# Define the conditions in desired order
conditions = ["common", "math", "adversarial", "parametrization", "linguistic_obfuscation"]

# Calculate averages and permutation tests for model results
model_averages, model_matrix = calculate_averages_and_differences(model_results_df, conditions, max_problems=5)

# Calculate averages and permutation tests for human results
human_averages, human_matrix = calculate_averages_and_differences(human_results_df, conditions, max_problems=7)

# Convert the matrices to LaTeX tables
model_latex_table = matrix_to_latex(model_averages, model_matrix, conditions, "Model Results")
human_latex_table = matrix_to_latex(human_averages, human_matrix, conditions, "Human Results")

# Print the LaTeX tables
print("\\subsection{Model Results LaTeX Table}")
print(model_latex_table)
print("\n\\subsection{Human Results LaTeX Table}")
print(human_latex_table)