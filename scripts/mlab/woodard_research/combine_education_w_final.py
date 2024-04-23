import pandas as pd
excel_file = '/Users/beja/Desktop/personal/Internet Access Disparities/Internet-Access-Disparities/datasets/CENSUS/US/Education.xlsx'
df_excel = pd.read_excel(excel_file)
csv_file = '/Users/beja/Desktop/personal/Internet Access Disparities/Internet-Access-Disparities/results/mlab/US/Woodard_research/MLAB_Woodard_w_census_2020_2024.csv'
df_csv = pd.read_csv(csv_file)

# Prepare the Excel data: convert 'FIPS Code' to string and remove trailing zeroes (if necessary)
df_excel['FIPS'] = df_excel['FIPS'].astype(str).str.rstrip('.0')

# Prepare the CSV data: convert 'geoid' to string and remove trailing zeroes
df_csv['geoid'] = df_csv['geoid'].astype(str).str.rstrip('.0')

# Define the columns to merge from Excel
columns_to_merge = [
    'Less_than_a_high_school_diploma_2017_21',
    'High_school_diploma_only_2017_21',
    'Some_college_or_associate_degree_2017_21',
    'Bachelor_degree_or_higher_2017_21',
    'Percent_of_adults_with_less_than_a_high_school_diploma_2017_21',
    'Percent_of_adults_with_a_high_school_diploma_only_2017_21',
    'Percent_of_adults_completing_some_college_or_associate_degree_2017_21',
    'Percent_of_adults_with_a_bachelor_degree_or_higher_2017_21'
]

# Merge the data on the FIPS
df_merged = pd.merge(df_csv, df_excel[['FIPS'] + columns_to_merge], left_on='geoid', right_on='FIPS', how='left')

# Drop the extra 'FIPS' column from the merge
df_merged.drop('FIPS', axis=1, inplace=True)

# Save the merged data to a new CSV file
output_file = 'merged_output.csv'  # You can choose a different file name
df_merged.to_csv(output_file, index=False)

print('Merge completed and saved to:', output_file)
