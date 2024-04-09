import pandas as pd

woodard_dataset_county_wise = '../../../datasets/Woodard nations/Woodard counties per nation.csv'
master_census_dataset_county_wise = '../../../results/mlab/US/Yearly Masters/combined_data.csv'
output_file_path = '../../../datasets/Woodard nations/merged_w_census_2020_2024_MLAB.csv'

# Reading the CSV files
df1 = pd.read_csv(woodard_dataset_county_wise)
df2 = pd.read_csv(master_census_dataset_county_wise)


df1['merge_key'] = df1['COUNTY NAME (SHORT)'] + df1['STATE NAME']
df2['merge_key'] = df2['county'] + df2['state_name']

# Merging the dataframes on the new combined key
merged_df = df2.merge(df1[['merge_key', 'WOODARD NATION NAME']], on='merge_key', how='left')

# Dropping the 'merge_key' column as it's redundant after merge
merged_df.drop('merge_key', axis=1, inplace=True)

# Saving the merged dataframe to a new CSV file
merged_df.to_csv(output_file_path, index=False)
