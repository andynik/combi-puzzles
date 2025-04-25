# Code to check model outputs in semi-automated way
# Code was modified to accept only IsCorrect data

import os
import csv
import re
import datetime


# Function to parse TXT files and extract puzzle statement and model outputs
def parse_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    puzzle_statement = content.split('\n')[1]

    pattern = re.compile(r'--- Model (.+?) output\. RUN \d+ ---\n((.|\n)+?)\n(?=(--- Model|$))', re.DOTALL)
    matches = pattern.findall(content)

    model_outputs = []
    for match in matches:
        model_outputs += [match[1]]

    return puzzle_statement, model_outputs

# Function to extract model name from model output line
def extract_model_name(model_output_line):
    match = re.search(r'Model (\S+) output', model_output_line)
    if match:
        return match.group(1)
    else:
        return "Unknown_Model"

# Function to get user input for two questions
def get_user_input():
    # is_correct = input("1) Is correct? (1 for Yes, 0 for No): ")
    # is_short = input("2) Is short? (1 for Yes, 0 for No): ")
    combined_response = input("\nIs correct? (1 for Yes, 0 for No): ")
    is_correct = combined_response[0]

    return is_correct


# Function to write data to CSV file
def write_to_csv(csv_file, data):
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Function to break too long output lines
def text_break_and_output(text, max_width=80):
    if len(text) < 80:
        print(text)
        return

    words = text.split()
    lines = []
    current_line = ''
    for word in words:
        if len(current_line) + len(word) + 1 <= max_width:
            current_line += word + ' '
        else:
            lines.append(current_line.strip())
            current_line = word + ' '
    if current_line:
        lines.append(current_line.strip())

    for line in lines:
        print(line)


# Main script
current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
outputs_path = 'outputs/experiment_prmpt_5'  # Path prompt dir with models/outputs
csv_file_path = 'responses_' + str(current_date) + '.csv'  # Replace with desired CSV file path

# Create or overwrite the CSV file
with open(csv_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Puzzle_ID', 'Model_Name', 'Run #', 'Is_Correct'])

for model_name in os.listdir(outputs_path):
    directory_path = outputs_path + '/' + model_name

    # Count how many rows to process Is_Short
    num_of_runs = 5
    cnt_total = len(os.listdir(directory_path)) * num_of_runs
    print("Prompts to check for model " + model_name + ":", cnt_total)

    cnt = 0
    # Iterate through TXT files in the directory
    for filename in os.listdir(directory_path):
        print('\nPuzzle info:', filename)
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)

            # Parse the TXT file
            puzzle_statement, model_outputs = parse_txt_file(file_path)

            # Iterate through model outputs
            for index, model_output in enumerate(model_outputs, start=0):
                cnt += 1
                # print(f"\nPuzzle Statement:\n{puzzle_statement}")
                # print(f"Model Output {index}:\n{model_output}")

                print("\nPuzzle Statement:")
                text_break_and_output(puzzle_statement)
                print("\nModel Output:" + " (run " + str(index) + ") " + str(cnt) + "/" + str(cnt_total))
                text_break_and_output(model_output)

                # Get user input for two questions
                is_correct = get_user_input()

                # Write data to CSV file
                puzzle_id = filename.replace('.txt', '')
                data = [puzzle_id, model_name, index, is_correct]
                write_to_csv(csv_file_path, data)

print("\nCheck completed.")
