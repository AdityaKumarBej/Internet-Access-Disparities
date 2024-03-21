import pandas as pd
import os, json

TYPE = "mobile"
YEAR = "2023"
# Path to the JSON file with state FIPS codes
STATE_FIPS_FILE_PATH = "/Users/beja/Desktop/Classes/Winter'24/project/Internet-Access-Disparities/datasets/Regions/US_state_fips.json"
# Placeholder for the base directory path where the state folders are located
BASE_RESULTS_FOLDER = f"/Users/beja/Desktop/Classes/Winter'24/project/Internet-Access-Disparities/results/ookla/USA/type={TYPE}"

# Placeholder for the state FIPS codes and names mapping
# Normally, you would load this from the USA_state_fips.json file
with open(STATE_FIPS_FILE_PATH, 'r') as f:
    state_fips = json.load(f)

# Initialize an empty DataFrame to hold all the combined data
combined_data = pd.DataFrame()

# Loop through the state FIPS dictionary
for state_name, fips_code in state_fips.items():
    # Construct the file path for the 2023 CSV file for the current state
    file_path = os.path.join(BASE_RESULTS_FOLDER, f"{state_name}-{fips_code}", YEAR , f"{YEAR}_average_stats.csv")
    print("the file path is ---- ", file_path)
    # Check if the file exists
    if os.path.exists(file_path):
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Add a column for the state name
        df['State'] = state_name
        df['Year'] = YEAR
        
        # Append the data to the combined DataFrame
        combined_data = pd.concat([combined_data, df], ignore_index=True)

# # Save the combined DataFrame to a new master CSV file
master_csv_path = f"/Users/beja/Desktop/Classes/Winter'24/project/Internet-Access-Disparities/results/ookla/USA/type={TYPE}/{YEAR}_master.csv"
combined_data.to_csv(master_csv_path, index=False)

print(f"Master CSV file has been saved to: {master_csv_path}")
