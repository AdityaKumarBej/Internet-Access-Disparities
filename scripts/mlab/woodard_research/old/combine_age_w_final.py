import pandas as pd

csv_age_file = '/Users/beja/Desktop/personal/Internet Access Disparities/Internet-Access-Disparities/datasets/CENSUS/US/Age.csv'
csv_mlab_file = '/Users/beja/Desktop/personal/Internet Access Disparities/Internet-Access-Disparities/results/mlab/US/Woodard_research/mlab_woodard_w_census_and_education.csv'

df_age = pd.read_csv(csv_age_file)
df_mlab = pd.read_csv(csv_mlab_file)

# Filter the age data to only include records where YEAR = 3
df_age = df_age[df_age['YEAR'] == 3]

# Select only the required columns in the age data
df_age = df_age[['geoid', 'MEDIAN_AGE_TOT', 'MEDIAN_AGE_MALE', 'MEDIAN_AGE_FEM']]

# Make sure the 'geoid' in df_age is a string and remove only leading zeros
df_age['geoid'] = df_age['geoid'].astype(str).str.lstrip('0')

# Make sure the 'geoid' in df_mlab is also a string
df_mlab['geoid'] = df_mlab['geoid'].astype(str)

# Merge the mlab data with the filtered and processed age data
df_merged = pd.merge(df_mlab, df_age, on='geoid', how='left')

# Output the results to a new CSV file
output_csv_path = 'merged_mlab_age_data.csv'
df_merged.to_csv(output_csv_path, index=False)

print(f'Merged data saved to {output_csv_path}')
