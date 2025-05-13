import pandas as pd

isp_file_path = '../../../datasets/ISP/bdc_us_provider_summary_by_geography_D23_17sep2024.csv'
isp_details_file_path = '../../../datasets/ISP/bdc_us_fixed_broadband_provider_summary_D23_17sep2024.csv'

df = pd.read_csv(isp_file_path, low_memory=False)
isp_df = pd.read_csv(isp_details_file_path, low_memory=False)

isp_df = isp_df[['provider_id', 'holding_company']].drop_duplicates()

filtered_df = df[
    (df['geography_type'] == "County") & 
    (df['data_type'] == "Fixed Broadband") & 
    (df['geography_id'].str.startswith("36"))
    ]

# print(filtered_df)

# value_counts stores in desc order
provider_counts = filtered_df['provider_id'].value_counts().reset_index()
provider_counts.columns = ['provider_id', 'frequency']
    
provider_counts_names = provider_counts.merge(
    isp_df[['provider_id', 'holding_company']], 
    on='provider_id', 
    how='left'
)
top_providers = provider_counts_names.head(9)

print("Provider ID, Provider Name, Frequency")
for _, row in top_providers.iterrows():
    print(f"{row['provider_id']}, {row['holding_company']}, {row['frequency']}")
