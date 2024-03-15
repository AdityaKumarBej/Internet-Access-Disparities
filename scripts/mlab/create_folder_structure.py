import os
import csv

master_file = '../../results/mlab/USA/Master_2020_2024_US_state_county.csv'
with open(master_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    data_by_state_year = {}
    for row in reader:
        state = row['state_name']
        state_code = row['state']
        year = row['year']
        
        state_folder = os.path.join("../../results/mlab/USA", f"{state}-{state_code}")
        if not os.path.exists(state_folder):
            os.makedirs(state_folder)

        year_folder = os.path.join(state_folder, year)
        if not os.path.exists(year_folder):
            os.makedirs(year_folder)

        state_year_file = os.path.join(year_folder, f"{year}_average_stats.csv")
        if state_year_file not in data_by_state_year:
            data_by_state_year[state_year_file] = []
        data_by_state_year[state_year_file].append(row.values())
        
    for year_file, data_rows in data_by_state_year.items():
        with open(year_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row.keys())
            writer.writerows(data_rows)

