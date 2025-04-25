# Avg vals for different models -- latex table (no p-vals)

import pandas as pd

# Define the CSV file that contains the model descriptions
runs_file = 'runs.csv'

# Read the description file
runs_df = pd.read_csv(runs_file)

# Filter out humans and normalize the scores
runs_df = runs_df[runs_df['model_name'] != 'humans']


def normalize_scores(score, model_name):
    # Normalize score by dividing by 5.0 if "gpt" or "llama3.1" is in model_name, otherwise divide by 10.0
    if 'gpt' in model_name.lower() or 'llama3.1' in model_name.lower():
        return score / 5.0
    else:
        return score / 10.0

def format_model_name(name):
    parts = name.split('_')
    model_type = parts[-1].upper()  # Get the model type and turn it to uppercase for consistent formatting
    prompt_num = parts[1]  # Get the number
    return f"{model_type}: prmpt-{prompt_num}"

# Extract variations and initialize scores dictionary
variations_columns = ["common", "math", "adversarial", "parametrization", "linguistic_obfuscation"]
models_scores = {model: {var: None for var in variations_columns} for model in runs_df['model_name'].unique()}

# Process each run and calculate normalized scores
for _, run in runs_df.iterrows():
    model_name = run['model_name']
    file_path = run['path']
    results_df = pd.read_csv(file_path)

    # Normalize 'Is_Correct' and add 'Variation' column based on 'Puzzle_ID'
    results_df['Is_Correct'] = normalize_scores(results_df['Is_Correct'], model_name)
    results_df['Variation'] = results_df['Puzzle_ID']

    # Group by 'Variation' and calculate normalized mean
    for var in variations_columns:
        if var.lower().replace(' ', '') in models_scores[model_name]:
            filtered_df = results_df[results_df['Variation'].str.contains(var, case=False)]
            models_scores[model_name][var] = filtered_df['Is_Correct'].mean()

# Generate LaTeX code
latex_string = "\\begin{table}\n"
latex_string += "\\centering\n"
latex_string += "\\begin{tabular}{l" + " c" * (len(variations_columns) + 1) + "}\n"  # Add one more 'c' for the new average column

# Convert each item in the list to capitalize the first letter and remove underscores
variations_columns = [column.replace("_", " ").capitalize() for column in variations_columns]

# Header row
header_row = "Model & " + " & ".join(variations_columns) + " & Overall \\\\\n"  # Include 'Average' in the header
latex_string += "\\hline\n"  # Add a horizontal line before the header
latex_string += header_row
latex_string += "\\hline\n"  # Add a horizontal line after the header

model_names_sorted = sorted(models_scores.keys(), key=lambda x: (x.split('_')[1], x.split('_')[0]))  # Sort by prompt number and then by the model type

for model in model_names_sorted:
    formatted_model_name = format_model_name(model)  # Format the model name
    scores = models_scores[model]
    valid_scores = [score for score in scores.values() if score is not None]  # Extract only non-None scores
    average_score = sum(valid_scores) / len(valid_scores) if valid_scores else None  # Compute the average; handle division by zero if there are no valid scores
    row = formatted_model_name + " & " + " & ".join(
        f"{score:.2f}" if score is not None else "-" for score in valid_scores)  # Format individual scores
    row += f" & {average_score:.2f}" if average_score is not None else " & -"  # Add formatted average score
    row += " \\\\\n"  # Add newlines and escape backslashes
    latex_string += row

latex_string += "\\hline\n"  # Add a horizontal line at the end
latex_string += "\\end{tabular}\n"
latex_string += "\\end{table}"

# Print the custom LaTeX formatted table
print(latex_string)