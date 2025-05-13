# step 6: Add ISP data to the merged dataset 

import pandas as pd

input_file = "../../../datasets/ISP/bdc_us_provider_summary_by_geography_D23_17sep2024.csv"
data = pd.read_csv(input_file)

county_data = data[(data['geography_type'] == 'County') & (data['data_type'] == 'Fixed Broadband')]

provider_counts = county_data.groupby('geography_id')['provider_id'].nunique().reset_index()

provider_counts = provider_counts.merge(county_data[['geography_id', 'geography_desc']].drop_duplicates(), 
                                        on='geography_id', how='left')

provider_counts['geography_id'] = provider_counts['geography_id'].astype(str).str.lstrip('0')

provider_counts.columns = ['GEOID', 'total_providers', 'isp_county_name']

# output_file = '../../../datasets/ISP/providers_by_county.csv'
# provider_counts.to_csv(output_file, index=False)

# print(f"CSV file created: {output_file}")

ookla_file = "../../../results/ookla/US/woodard_research/ookla_fixed_woodard_race_gender_age_density.csv"
ookla_data = pd.read_csv(ookla_file)

ookla_data['GEOID'] = ookla_data['GEOID'].astype(str).str.lstrip('0')

merged_data = ookla_data.merge(provider_counts[['GEOID', 'total_providers']], on='GEOID', how='left')

output_file = "../../../results/ookla/US/woodard_research/ookla_fixed_woodard_census_providers.csv"

merged_data.to_csv(output_file, index=False)

