# Code to check results after model re-run

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
    combined_response = input("\nIs correct? Is short? (1 for Yes, 0 for No): ")
    is_correct, is_short = combined_response[0], combined_response[1]

    return is_correct, is_short

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

# Dir with output files (all)
prompt_path = 'outputs/1_checked/experiment_prmpt_5_the_short_and_correct_answer_is/'
model_name = 'mixtral-8x7b-ins'
output_files_path = prompt_path + model_name

# File with results old
file_to_check_path = 'mixtral_checks_merged.csv'

# File with results new
fine_upd_path = 'responses_' + str(current_date) + '_upd.csv'

# Create upd CSV file
with open(fine_upd_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Puzzle_ID', 'Model_Name', 'Run #', 'Is_Correct', 'Is_Short'])

# Count how many rows to process Is_Short
cnt_total = 0
with open(file_to_check_path, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['Is_Correct'] == '1':
            puzzle_id = row['Puzzle_ID']
            cnt_total += 1
print(cnt_total)

# Checking old results
cnt = 0
with open(file_to_check_path, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['Is_Correct'] == '1':
            puzzle_id = row['Puzzle_ID']
            puzzle_file_name = f'{puzzle_id}.txt'

            print('\nPuzzle info:', puzzle_id)

            file_path = output_files_path + '/' + puzzle_file_name

            # Parse the TXT file
            puzzle_statement, model_outputs = parse_txt_file(file_path)

            # Iterate through model outputs
            for index, model_output in enumerate(model_outputs, start=0):
                if str(index) == str(row['Run #']):
                    cnt += 1
                    print("\nPuzzle Statement:")
                    text_break_and_output(puzzle_statement)

                    print("\nModel Output:" + " (run " + str(index) + ") " + str(cnt) + "/" + str(cnt_total))
                    text_break_and_output(model_output)

                    # Get user input for two questions

                    is_correct, is_short = get_user_input()

                    # Write data to CSV file
                    puzzle_id = puzzle_file_name.replace('.txt', '')
                    data = [puzzle_id, model_name, index, is_correct, is_short]
                    write_to_csv(fine_upd_path, data)

print("\nCheck completed.")
