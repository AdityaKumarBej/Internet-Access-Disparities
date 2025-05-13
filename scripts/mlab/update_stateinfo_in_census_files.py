# Adding state names and numbers to the M-LAB dataset (only codes are available in the census dataset)

import csv
import json

def add_state_info(input_csv_path, output_csv_path, json_path, new_column_name):
    with open(json_path) as f:
        state_codes = json.load(f)
    state_codes = {v: k for k, v in state_codes.items()}

    def update_row(row):
        updated_row = row[:]
        if updated_row[2] in state_codes:
            new_value = state_codes[updated_row[2]]
            updated_row.insert(3, new_value)
        return updated_row

    with open(input_csv_path, newline='') as inputcsvfile, \
         open(output_csv_path, 'w', newline='') as outputcsvfile:
        reader = csv.reader(inputcsvfile)
        writer = csv.writer(outputcsvfile)
        for i, row in enumerate(reader):
            if i == 0:
                header_row = row[:]
                header_row.insert(3, new_column_name)
                writer.writerow(header_row)
            else:
                writer.writerow(update_row(row))

# add state names using state codes
add_state_info(
    input_csv_path='../../datasets/M-LAB/IN/Master_2020_2024_IN_statecode.csv',
    output_csv_path='../../datasets/M-LAB/IN/Master_2020_2024_IN_state.csv',
    json_path='../../datasets/Regions/IN_state_codes.json',
    new_column_name='state_name'
)

# add state numbers
# add_state_info(
#     input_csv_path='../../datasets/M-LAB/IN/Master_2020_2024_IN_state.csv',
#     output_csv_path='../../datasets/M-LAB/IN/Master_2020_2024_IN_state_number.csv',
#     json_path='../../datasets/Regions/IN_state_numbers.json',
#     new_column_name='state_number'
# )