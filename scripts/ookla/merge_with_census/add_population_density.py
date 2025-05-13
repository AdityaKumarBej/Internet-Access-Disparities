# step 5: add education attributes to ookla measurement file after adding woodard nations, race, gender, age, and edu

import pandas as pd
import geopandas as gpd

input_csv = '../../../results/ookla/US/woodard_research/ookla_fixed_woodard_race_gender_age_edu.csv'
census_file = '../../../datasets/census/US/regions/tl_2023_us_county.zip'

output_csv = '../../../results/ookla/US/woodard_research/ookla_mobile_woodard_race_gender_age_edu_density.csv'

ookla_df = pd.read_csv(input_csv)
census_df = gpd.read_file(census_file)

ookla_df['GEOID'] = ookla_df['GEOID'].astype(str)
census_df['GEOID'] = census_df['GEOID'].astype(str).str.lstrip('0')

merged_df = pd.merge(ookla_df, census_df[['GEOID', 'ALAND']], on='GEOID', how='left')

merged_df['land_area'] = merged_df['ALAND'] / 1000000
merged_df['population_density'] = merged_df['TOT_POP'] / merged_df['land_area']

merged_df = merged_df.drop(columns=['ALAND'])

merged_df.to_csv(output_csv, index=False)
print(f'Complete and saved in {output_csv}.')