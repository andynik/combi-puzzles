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


# Function to calculate the permutation tests for all condition pairs
def calculate_permutation_tests(df, conditions):
    matrix = pd.DataFrame(index=conditions, columns=conditions)

    for condition1 in conditions:
        for condition2 in conditions:
            if condition1 != condition2:
                group1 = df[df['Puzzle_ID'].str.contains(condition1)]['Is_Correct']
                group2 = df[df['Puzzle_ID'].str.contains(condition2)]['Is_Correct']
                diff, p_val = permutation_test(group1.values, group2.values)
                matrix.loc[condition1, condition2] = f'{diff:.2f}, {p_val:.4f}'
            else:
                matrix.loc[condition1, condition2] = "/"  # diagonal values are not compared
    return np.tril(matrix)


# Read in the data
model_results_df = pd.read_csv('results_csv/model_results.csv')
human_results_df = pd.read_csv('results_csv/human_results.csv')

# Define the conditions
conditions = ["common", "math", "adversarial", "parametrization", "linguistic_obfuscation"]

# Calculate the permutation tests for the model results
model_matrix = calculate_permutation_tests(model_results_df, conditions)

# Calculate the permutation tests for the human results
human_matrix = calculate_permutation_tests(human_results_df, conditions)

matrix_str = "\\begin{table}[htbp]\n\\centering\n"
matrix_str += "\\begin{adjustbox}{width=1\\textwidth}\n"
matrix_str += "\\begin{tabular}{" + " l" + " c" * len(conditions) + " }\n\\toprule\n"

# Create the header row
header_row = " & " + " & ".join(["\\textbf{" + cond + "}" for cond in conditions]) + " \\\\\n\\midrule\n"
matrix_str += header_row


# Define a function to convert p-values to significance level strings
def matrix_to_latex(matrix, conditions, caption):
    matrix_str = "\\begin{table}[h]\n"
    matrix_str += "\\centering\n"
    matrix_str += "\\begin{tabular}{l" + "c" * len(conditions) + "}\n"
    matrix_str += "\\hline\n"

    # Create the header row
    header_row = " & " + " & ".join([cond.replace("_", " ").capitalize() for cond in conditions]) + " \\\\\n"
    matrix_str += header_row
    matrix_str += "\\hline\n"

    # Define a function to convert p-values to significance level strings
    def significance_level(p_value):
        if p_value < 0.001:
            return '***'  # p < 0.001
        elif p_value < 0.01:
            return '**'  # p < 0.01
        elif p_value < 0.05:
            return '*'   # p < 0.05
        else:
            return 'n.s.'  # Not significant

    # Iterate over the matrix and fill the LaTeX table with significance levels
    for i, condition in enumerate(conditions):
        row_values = [condition.replace("_", " ").capitalize()]  # Start row with condition name
        for j in range(len(conditions)):
            if j < i:
                # Get the p-value, which is stored in the lower triangle of the matrix

                # exact values
                p_value = str(matrix[i, j].split(",")[1]) # to show only p-vals
                row_values.append(p_value)

                # significance values
                # Convert the p-value to a significance level string
                # p_value = float(matrix[i, j].split(",")[1])
                # row_values.append(significance_level(p_value))
            elif j == i:
                # Diagonal values (same condition comparison)
                row_values.append('-')
            else:
                # Upper triangle of table blank if only lower triangle is populated with p-values
                row_values.append('')

        # Join the row values and add them to the matrix string
        matrix_str += " & ".join(row_values) + " \\\\\n"

    matrix_str += "\\hline\n"
    matrix_str += "\\end{tabular}\n"
    matrix_str += f"\\caption{{{caption}}}\n"
    matrix_str += "\\end{table}\n"

    return matrix_str


# Convert the matrices to LaTeX tables
model_latex_table = matrix_to_latex(model_matrix, conditions, "Model Results Comparison")
human_latex_table = matrix_to_latex(human_matrix, conditions, "Human Results Comparison")

# Print the LaTeX tables
print("\subsection{Model Results LaTeX Table}")
print(model_latex_table)
print("\n\subsection{Human Results LaTeX Table}")
print(human_latex_table)