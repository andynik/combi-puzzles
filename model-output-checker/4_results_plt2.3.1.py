# Per puzzle / Conditions avg -- for Is_Correct data only for Humans + Model
# "parametrization" -> "parameterisation"


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

# Constants
model_name = "model"
human_name = "human"

model_num_of_runs = 5
human_num_of_runs = 5

# Read the CSV files
df_model = pd.read_csv(model_name + "_results.csv")
df_human = pd.read_csv(human_name + "_results_top5.csv")

# Function to extract puzzle IDs and variations
def extract_puzzle_info(df):
    puzzle_ids = df['Puzzle_ID'].str.extract(r'_p(\d+)_v(\w+)$')
    df['Puzzle_Number'] = puzzle_ids[0].astype(int)
    df['Variation'] = puzzle_ids[1]
    return df

# Extract puzzle info for both datasets
df_model = extract_puzzle_info(df_model)
df_human = extract_puzzle_info(df_human)

# Define colors for each variation
variation_colors = {
    'adversarial': 'red',
    'common': 'gray',
    'linguistic_obfuscation': 'purple',
    'math': 'blue',
    'parametrization': 'green'
}

# Create figure and subplots
fig, (ax1, ax3) = plt.subplots(1, 2, figsize=(16, 6))

# Model results: Puzzles
for variation, color in variation_colors.items():
    for puzzle_id in range(1, 26):
        puzzle_data_model = df_model[(df_model['Puzzle_Number'] == puzzle_id) & (df_model['Variation'] == variation)]
        x_values_model = puzzle_id + np.random.uniform(-0.2, 0.2, len(puzzle_data_model))
        ax1.plot(x_values_model, puzzle_data_model['Is_Correct'], 'o', markersize=8, color=color)
ax1.set_xlabel('Puzzle ID')
ax1.set_ylabel('Score')
ax1.set_xticks(range(1, 26))
ax1.set_ylim(-0.5, model_num_of_runs + 0.5)
ax1.set_yticks(np.linspace(0, model_num_of_runs, model_num_of_runs + 1))
ax1.grid(True)

# Add custom legend outside the plot + fixing the labelnames
handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=8) for color in variation_colors.values()]
variation_colors_fixed = {
    'adversarial': 'red',
    'common': 'gray',
    'ling.obfus.': 'purple',
    'math': 'blue',
    'param.': 'green'
}
labels = list(variation_colors_fixed.keys())
ax1.legend(handles, labels, loc='lower left')

# Human results: Puzzles
for variation, color in variation_colors.items():
    for puzzle_id in range(1, 26):
        puzzle_data_human = df_human[(df_human['Puzzle_Number'] == puzzle_id) & (df_human['Variation'] == variation)]
        x_values_human = puzzle_id + np.random.uniform(-0.2, 0.2, len(puzzle_data_human))
        ax3.plot(x_values_human, puzzle_data_human['Is_Correct'], 'o', markersize=8, color=color)
ax3.set_xlabel('Puzzle ID')
ax3.set_ylabel('Score')
ax3.set_xticks(range(1, 26))
ax3.set_ylim(-0.5, human_num_of_runs + 0.5)
ax3.set_yticks(np.linspace(0, human_num_of_runs, human_num_of_runs + 1))
ax3.grid(True)
ax3.legend(handles, labels, loc='lower left')

# Add labels "Human pupils" and "Model" in top-right corners of specified subplots
ax3.annotate('Human participants', xy=(1, 1), xycoords='axes fraction', fontsize=15, fontweight='regular', ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.3', color='white', alpha=0.6))
ax1.annotate('GPT-4 model', xy=(1, 1), xycoords='axes fraction', fontsize=15, fontweight='regular', ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.3', color='white', alpha=0.6))

# Adjust layout
plt.tight_layout()
plt.show()