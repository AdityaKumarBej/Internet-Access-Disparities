import pandas as pd

input_file = '../../../results/ookla/US/cbg/raw_masters/state_master_fixed_06.csv'
nation_file = '../../../datasets/census/US/regions/woodard_countywise_california_fips.csv'
output_file = '../../../results/ookla/US/cbg/raw_masters/state_master_fixed_06_nations.csv'

data_df = pd.read_csv(input_file)
nation_df = pd.read_csv(nation_file)

nation_df.drop(columns=['COUNTY NAME (SHORT)', 'COUNTY NAME (FULL)', 'STATE NAME'], inplace=True)

# print(nation_df)

merged_df = pd.merge(data_df, nation_df, how='left', left_on='COUNTYFP', right_on='COUNTY_FIPS')

merged_df['nation_name'] = merged_df['WOODARD NATION NAME']
merged_df.drop(columns=['WOODARD NATION NAME'], inplace=True)

merged_df.to_csv(output_file, index=False)

print(f"File with nations column saved to: {output_file}")

