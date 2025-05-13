# step 3: add age attributes to ookla measurement file after adding woodard nations, race and gender

import pandas as pd

# Load race.csv and mlab.csv
age_df = pd.read_csv("../../../datasets/CENSUS/US/Age_geoid.csv")
ookla_df = pd.read_csv("../../../results/ookla/USA/Woodard_research/ookla_mobile_woodard_race_gender.csv")

# Filter age data for the year 2021
df_filtered = age_df[age_df['YEAR'] == 3]

# Select only the required columns in the race data
required_columns = ['geoid','MEDIAN_AGE_TOT', 'POPESTIMATE', 'UNDER5_TOT', 'AGE513_TOT', 'AGE1417_TOT', 'AGE1824_TOT', 'AGE2544_TOT', 'AGE4564_TOT', 'AGE65PLUS_TOT']
df_filtered = df_filtered[required_columns]

# Merge the mlab data with the filtered and processed race data
df_merged = pd.merge(ookla_df, df_filtered, left_on='GEOID', right_on='geoid', how='left')

# Add new columns
df_merged['percentage_age_under_5'] = df_merged['UNDER5_TOT'] / df_merged['POPESTIMATE'] * 100
df_merged['percentage_age_5_17'] = (df_merged['AGE513_TOT'] + df_merged['AGE1417_TOT']) / df_merged['POPESTIMATE'] * 100
df_merged['percentage_age_18_64'] = (df_merged['AGE1824_TOT'] + df_merged['AGE2544_TOT'] + df_merged['AGE4564_TOT']) / df_merged['POPESTIMATE'] * 100
df_merged['percentage_age_over_65'] = df_merged['AGE65PLUS_TOT'] / df_merged['POPESTIMATE'] * 100

# Drop the unwanted columns
unwanted_columns = ['POPESTIMATE', 'POPESTIMATE', 'UNDER5_TOT', 'AGE513_TOT', 'AGE1417_TOT', 'AGE1824_TOT', 'AGE2544_TOT', 'AGE4564_TOT', 'AGE65PLUS_TOT']
df_merged.drop(columns=unwanted_columns, inplace=True)

# Write the updated DataFrame back to CSV
df_merged.to_csv("../../../results/ookla/USA/Woodard_research/ookla_mobile_woodard_race_gender_age.csv", index=False)
