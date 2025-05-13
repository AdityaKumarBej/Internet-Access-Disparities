# step 5: Add population density attribute to mlab dataset (aleready has race, gender, age and edu attributes)

import pandas as pd
import geopandas as gpd

input_csv = '../../../results/mlab/US/woodard_research/mlab_woodard_race_gender_age.csv'
census_file = '../../../datasets/census/US/regions/tl_2023_us_county.zip'

output_csv = '../../../results/mlab/US/mlab_census.csv'

mlab_df = pd.read_csv(input_csv)
census_df = gpd.read_file(census_file)

mlab_df['geoid'] = mlab_df['geoid'].astype(str)
census_df['GEOID'] = census_df['GEOID'].astype(str).str.lstrip('0')

merged_df = pd.merge(mlab_df, census_df[['GEOID', 'ALAND']], left_on='geoid', right_on='GEOID', how='left')

merged_df['land_area'] = merged_df['ALAND'] / 1000000
merged_df['population_density'] = merged_df['TOT_POP'] / merged_df['land_area']

merged_df = merged_df.drop(columns=['GEOID', 'ALAND'])

merged_df.to_csv(output_csv, index=False)
print(f'Complete and saved in {output_csv}.')