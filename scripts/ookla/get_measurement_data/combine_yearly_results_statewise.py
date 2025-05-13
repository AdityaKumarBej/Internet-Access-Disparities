# Step 1: Combine yearly results for each state into a single CSV file called "..._average_stats.csv" in the respective state folder.
# created files will be merged in different script

import os
import pandas as pd
import json

# Path to the JSON file with state FIPS codes
STATE_FIPS_FILE_PATH = "/Users/beja/Desktop/Classes/Winter'24/project/Internet-Access-Disparities/datasets/Regions/USA_state_fips.json"
# Base directory where state folders are located
BASE_RESULTS_FOLDER = "/Users/beja/Desktop/Classes/Winter'24/project/Internet-Access-Disparities/results/ookla/USA/type=fixed"

# Load state FIPS codes
with open(STATE_FIPS_FILE_PATH, 'r') as f:
    state_fips = json.load(f)

# Function to process each state
def process_state(state_name, fips_code):
    state_folder = f"{BASE_RESULTS_FOLDER}/{state_name}-{fips_code}"
    # print("the state folder is ---- ", state_folder)
    all_years_data = []

    for year in range(2019, 2024):  # 2019 to 2023
        csv_path = f"{state_folder}/{year}/{year}_average_stats.csv"
        if os.path.exists(csv_path):
            year_data = pd.read_csv(csv_path)
            year_data['year'] = year
            all_years_data.append(year_data)

    if all_years_data:
        consolidated_df = pd.concat(all_years_data, ignore_index=True)
        consolidated_csv_path = f"{state_folder}/Consolidated_CSV.csv"
        consolidated_df.to_csv(consolidated_csv_path, index=False)
        print(f"Consolidated CSV saved for {state_name} at {consolidated_csv_path}")
    else:
        print(f"No data found for {state_name}")

# Iterate over each state and process
for state_name, fips_code in state_fips.items():
    process_state(state_name, fips_code)
