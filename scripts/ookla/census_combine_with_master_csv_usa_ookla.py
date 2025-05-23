import pandas as pd

# Paths to the input files
TYPE = "mobile"
YEAR = "2023"
population_estimates_path = "/Users/beja/Desktop/Classes/Winter'24/project/Internet-Access-Disparities/datasets/CENSUS/US/PopulationEstimates.xlsx"
unemployment_path = "/Users/beja/Desktop/Classes/Winter'24/project/Internet-Access-Disparities/datasets/CENSUS/US/Unemployment.xlsx"
master_csv_path = f"/Users/beja/Desktop/Classes/Winter'24/project/Internet-Access-Disparities/results/ookla/USA/type={TYPE}/{YEAR}_master.csv"

# Read the data from the Excel and CSV files
population_estimates = pd.read_excel(population_estimates_path)
unemployment = pd.read_excel(unemployment_path)
master_csv = pd.read_csv(master_csv_path)

# Prepare the FIPS codes (remove leading zeros and ensure they are strings)
population_estimates['FIPStxt'] = population_estimates['FIPStxt'].astype(str).str.lstrip('0')
unemployment['FIPS_Code'] = unemployment['FIPS_Code'].astype(str).str.lstrip('0')
master_csv['GEOID'] = master_csv['GEOID'].astype(str).str.lstrip('0')

# Extract the required columns
population_data = population_estimates[['FIPStxt', 'POP_ESTIMATE_2022', 'NET_MIG_2022']]
unemployment_data = unemployment[['FIPS_Code', 'Median_Household_Income_2021', 'Med_HH_Income_Percent_of_State_Total_2021']]

# Merge the population and unemployment data with the master CSV based on the FIPS/GEOID keys
merged_data = master_csv.merge(population_data, left_on='GEOID', right_on='FIPStxt', how='left')
merged_data = merged_data.merge(unemployment_data, left_on='GEOID', right_on='FIPS_Code', how='left')

# Drop the extra FIPS columns if needed
merged_data.drop(['FIPStxt', 'FIPS_Code'], axis=1, inplace=True)

# Save the merged data to a new CSV file
output_path = f"/Users/beja/Desktop/Classes/Winter'24/project/Internet-Access-Disparities/results/ookla/USA/type={TYPE}/Yearly Masters/{YEAR}_master_w_census.csv"
merged_data.to_csv(output_path, index=False)
