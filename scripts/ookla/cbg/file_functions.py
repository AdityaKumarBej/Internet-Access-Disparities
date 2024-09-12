import os
import pandas as pd

def create_master_file(service_type: str, state_fips: str, counties: list, region: str):
    folder_path = f'../../../results/ookla/US/cbg/census/'

    # List to hold dataframes
    df_list = []

    for county_fips in counties:
        file_pattern = f'ookla_{service_type}_cbg_{state_fips}_{county_fips}_census.csv'
    
        file_path = os.path.join(folder_path, file_pattern)
        
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path)
            df_list.append(df)

    master_df = pd.concat(df_list, ignore_index=True)

    new_region = region.replace(" ", "").lower()
    output_file_path = f'../../../results/ookla/US/cbg/masters/ookla_{service_type}_cbg_master_{state_fips}_{new_region}.csv'
    
    master_df.to_csv(output_file_path, index=False)

    print(f"Master CSV file has been created at: {output_file_path}")

# def create_master_file(service_type: str, state_fips: str):
#     folder_path = f'../../../results/ookla/US/cbg/census/'
#     file_pattern = f'ookla_{service_type}_cbg_{state_fips}'

#     # List to hold dataframes
#     df_list = []

#     for filename in os.listdir(folder_path):
#         if filename.startswith(file_pattern) and filename.endswith('.csv'):
            
#             filepath = os.path.join(folder_path, filename)
#             df = pd.read_csv(filepath)
#             df_list.append(df)

#     master_df = pd.concat(df_list, ignore_index=True)
#     output_file_path = os.path.join(folder_path, f'ookla_{service_type}_cbg_master_{state_fips}.csv')
#     master_df.to_csv(output_file_path, index=False)

#     print(f"Master CSV file has been created at: {output_file_path}")
