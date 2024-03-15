import csv
import json

with open('../../datasets/Regions/IN_state_codes.json') as f:
    state_codes = json.load(f)

state_codes = {v: k for k, v in state_codes.items()}

def update_state_name(row):
    updated_row = row[:]
    if updated_row[2] in state_codes:
        state_name = state_codes[updated_row[2]]
        # Insert state name next to state code
        updated_row.insert(3, state_name)
    return updated_row

with open('../../datasets/M-LAB/IN/2024_IN_statecode_city.csv', newline='') as inputcsvfile,\
     open('../../results/mlab/IN/Yearly Masters/2024_IN_state_city.csv', 'w', newline='') as outputcsvfile:
    reader = csv.reader(inputcsvfile)
    writer = csv.writer(outputcsvfile)
    for i, row in enumerate(reader):
        if i == 0:
            header_row = row
            header_row.insert(3, 'state_name')  # Insert state name column
            writer.writerow(header_row)
        else:
            writer.writerow(update_state_name(row))