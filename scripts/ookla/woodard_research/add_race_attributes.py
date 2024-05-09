import pandas as pd

# Load race.csv and mlab.csv
race_df = pd.read_csv("../../../datasets/CENSUS/US/Race_geoid.csv")
ookla_df = pd.read_csv("../../../results/ookla/USA/Woodard_research/ookla_fixed_woodard.csv")

# Filter the race data to only include records where year is 2023 and all age groups
race_filtered = race_df[(race_df['YEAR'] == 3) & (race_df['AGEGRP'] == 0)]

# Select only the required columns in the race data
race_filtered = race_filtered[['geoid','TOT_POP', 'TOT_MALE', 'TOT_FEMALE', 
'NHWA_MALE', 'NHWA_FEMALE', 'NHBA_MALE', 'NHBA_FEMALE', 'NHIA_MALE', 'NHIA_FEMALE', 'NHAA_MALE', 'NHAA_FEMALE', 'NHNA_MALE', 'NHNA_FEMALE',
'NHTOM_MALE', 'NHTOM_FEMALE', 'H_MALE', 'H_FEMALE']]

# Merge the mlab data with the filtered and processed race data
df_merged = pd.merge(ookla_df, race_filtered, left_on='GEOID', right_on='geoid', how='left')

# Add new columns
df_merged['total_white'] = df_merged['NHWA_MALE'] + df_merged['NHWA_FEMALE']
df_merged['total_black_or_african'] = df_merged['NHBA_MALE'] + df_merged['NHBA_FEMALE']
df_merged['total_american_indian_and_native_alaskan'] = df_merged['NHIA_MALE'] + df_merged['NHIA_FEMALE']
df_merged['total_asian'] = df_merged['NHAA_MALE'] + df_merged['NHAA_FEMALE']
df_merged['total_native_hawaiian_and_other_pacific_islander'] = df_merged['NHNA_MALE'] + df_merged['NHNA_FEMALE']
df_merged['total_two_or_more_races'] = df_merged['NHTOM_MALE'] + df_merged['NHTOM_FEMALE']

df_merged['total_hispanic'] = df_merged['H_MALE'] + df_merged['H_FEMALE']

df_merged['percentage_white'] = (df_merged['total_white'] / df_merged['TOT_POP']) * 100
df_merged['percentage_black_or_african'] = (df_merged['total_black_or_african'] / df_merged['TOT_POP']) * 100
df_merged['percentage_american_indian_and_native_alaskan'] = (df_merged['total_american_indian_and_native_alaskan'] / df_merged['TOT_POP']) * 100
df_merged['percentage_asian'] = (df_merged['total_asian'] / df_merged['TOT_POP']) * 100
df_merged['percentage_native_hawaiian_and_other_pacific_islander'] = (df_merged['total_native_hawaiian_and_other_pacific_islander'] / df_merged['TOT_POP']) * 100
df_merged['percentage_two_or_more_races'] = (df_merged['total_two_or_more_races'] / df_merged['TOT_POP']) * 100

df_merged['percentage_hispanic'] = (df_merged['total_hispanic'] / df_merged['TOT_POP']) * 100

df_merged['percentage_male'] = (df_merged['TOT_MALE'] / df_merged['TOT_POP']) * 100
df_merged['percentage_female'] = (df_merged['TOT_FEMALE'] / df_merged['TOT_POP']) * 100

# Drop the unwanted columns
df_merged.drop(columns=['geoid', 'NHWA_MALE', 'NHWA_FEMALE', 'NHBA_MALE', 'NHBA_FEMALE', 'NHIA_MALE', 'NHIA_FEMALE', 'NHAA_MALE', 'NHAA_FEMALE', 'NHNA_MALE', 'NHNA_FEMALE', 'NHTOM_MALE', 'NHTOM_FEMALE', 'H_MALE', 'H_FEMALE'], inplace=True)

# Write the updated DataFrame back to CSV
df_merged.to_csv("../../../results/ookla/USA/Woodard_research/ookla_fixed_woodard_race_gender.csv", index=False)


