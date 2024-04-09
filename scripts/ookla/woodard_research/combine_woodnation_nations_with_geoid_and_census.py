import pandas as pd

# Replace 'file1.csv' and 'file2.csv' with your actual file paths
woodard_dataset_county_wise = '/Users/adityabej/Desktop/Projects/internet_access_disparities/Internet-Access-Disparities/datasets/Woodard nations/Woodard counties per nation.csv'  # This should be the path to your first file
master_census_dataset_county_wise = '/Users/adityabej/Desktop/Projects/internet_access_disparities/Internet-Access-Disparities/results/ookla/USA/type=fixed/2019_2023_master_w_census.csv'  # This should be the path to your second file
output_file_path = '/Users/adityabej/Desktop/Projects/internet_access_disparities/Internet-Access-Disparities/datasets/Woodard nations/merged_w_census__2019_2023_OOKLA_updated.csv'  # Path for the output file

# Reading the CSV files
df1 = pd.read_csv(woodard_dataset_county_wise)
df2 = pd.read_csv(master_census_dataset_county_wise)

# Ensure state names in both dataframes are in the same format if necessary
# Example: df1['STATE NAME'] = df1['STATE NAME'].map(state_name_mapping)
# df2['State'] = df2['State'].map(state_name_mapping)
# This step might be unnecessary if state names are already in the same format

# Preparing for merge by ensuring both dataframes have compatible state name columns
# Note: Adjust the 'STATE NAME' and 'State' column names if they are different in your datasets
df1['merge_key'] = df1['COUNTY NAME (FULL)'] + df1['STATE NAME']
df2['merge_key'] = df2['NAMELSAD'] + df2['State']

# Merging the dataframes on the new combined key
merged_df = df2.merge(df1[['merge_key', 'WOODARD NATION NAME']], on='merge_key', how='left')

# Dropping the 'merge_key' column as it's redundant after merge
merged_df.drop('merge_key', axis=1, inplace=True)

# Saving the merged dataframe to a new CSV file
merged_df.to_csv(output_file_path, index=False)

print(f"Merged file saved as '{output_file_path}'.")