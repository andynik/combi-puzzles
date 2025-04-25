import pandas as pd
import numpy as np

# Load the data from the CSV file
data = pd.read_csv('solved.csv') # file with 1 and 0 -- indicating problems which has been solved by model/humans at least once

# Function to perform a permutation test
def perm_test(group1, group2, n_permutations=10000):
    observed_stat = np.mean(group1) - np.mean(group2)
    combined = np.concatenate([group1, group2])
    permuted_stats = np.zeros(n_permutations)

    for i in range(n_permutations):
        np.random.shuffle(combined)
        permuted_stats[i] = np.mean(combined[:len(group1)]) - np.mean(combined[len(group1):])

    p_value = np.mean(np.abs(permuted_stats) >= np.abs(observed_stat))
    return observed_stat, p_value

# Apply permutation test across each variation
variations = ['adv', 'common', 'obfus', 'math', 'param']
results = {}

for variation in variations:
    model_column = f'{variation}_model'
    human_column = f'{variation}_human'
    statistic, p_value = perm_test(data[model_column], data[human_column])
    results[variation] = {
        'statistic': statistic,
        'p_value': p_value
    }

# Calculate the overall permutation test across all variations
model_total = data[[f'{var}_model' for var in variations]].values.flatten()
human_total = data[[f'{var}_human' for var in variations]].values.flatten()
total_statistic, total_p_value = perm_test(model_total, human_total)

# Store the total results
results['total'] = {
    'statistic': total_statistic,
    'p_value': total_p_value
}

# Print the results
for variation, result in results.items():
    print(f"{variation.capitalize()} - Statistic: {result['statistic']}, p-value: {result['p_value']}")