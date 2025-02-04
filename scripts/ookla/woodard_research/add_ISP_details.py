import pandas as pd

input_file = "../../../datasets/ISP/bdc_us_provider_summary_by_geography_D23_17sep2024.csv"
ookla_file = "../../../results/ookla/US/woodard_research/ookla_fixed_woodard_census_providers.csv"
output_file = "ISP_details.csv"

# data = pd.read_csv(input_file)
data = pd.read_csv(input_file, dtype={'geography_id': str})

county_data = data[(data['geography_type'] == 'County') & (data['data_type'] == 'Fixed Broadband')]


# total availability in each county - sum up all 
cumulative_availability = county_data.groupby('geography_id')[['res_st_pct', 'bus_iv_pct']].sum().reset_index()
cumulative_availability.columns = ['geography_id', 'cumulative_res_st_pct', 'cumulative_bus_iv_pct']

county_data = data[(data['geography_type'] == 'County') & (data['data_type'] == 'Fixed Broadband')]

# max availability provider? 
max_res_provider = county_data.loc[
    county_data.groupby('geography_id')['res_st_pct'].idxmax()
][['geography_id', 'provider_id', 'res_st_pct']].reset_index(drop=True)
max_res_provider.columns = ['geography_id', 'max_residential_provider', 'max_residential_availability']

max_bus_provider = county_data.loc[
    county_data.groupby('geography_id')['bus_iv_pct'].idxmax()
][['geography_id', 'provider_id', 'bus_iv_pct']].reset_index(drop=True)
max_bus_provider.columns = ['geography_id', 'max_business_provider', 'max_business_availability']

max_provider = pd.merge(max_res_provider, max_bus_provider, on='geography_id', how='outer')

# merge cumulative availability and max provider information
result = pd.merge(cumulative_availability, max_provider, on='geography_id')

result.columns = [
    'GEOID', 
    'cumulative_res_st_pct', 'cumulative_bus_iv_pct', 
    'max_residential_provider', 'max_residential_availability', 
    'max_business_provider', 'max_business_availability'
]

# merge that to existing ookla file
ookla_data = pd.read_csv(ookla_file)

ookla_data['GEOID'] = ookla_data['GEOID'].astype(str).str.lstrip('0')
result['GEOID'] = result['GEOID'].astype(str).str.lstrip('0')

merged_data = ookla_data.merge(result, on='GEOID', how='left')

merged_data.to_csv(output_file, index=False)