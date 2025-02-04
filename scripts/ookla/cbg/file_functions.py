import os
import pandas as pd

def create_master_file(service_type: str, state_fips: str, counties: list, region: str):
    folder_path = f'../../../results/ookla/US/cbg/raw_census/'

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
    output_file_path = f'../../../results/ookla/US/cbg/raw_masters/ookla_{service_type}_cbg_master_{state_fips}_{new_region}.csv'
    
    master_df.to_csv(output_file_path, index=False)

    print(f"Master CSV file has been created at: {output_file_path}")

def create_state_master(service_type: str, state_fips: str):
    folder_path = f'../../../results/ookla/US/cbg/raw_census/'
    file_pattern = f'ookla_{service_type}_cbg_{state_fips}'
    output_file = f'../../../results/ookla/US/cbg/raw_masters/state_master_{service_type}_{state_fips}.csv'
    combined_data = []

    for file_name in os.listdir(folder_path):
        if file_pattern in file_name:

            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            combined_data.append(df)

    if combined_data:
        master_df = pd.concat(combined_data, ignore_index=True)
        
        master_df.to_csv(output_file, index=False)
        print(f"Master file created: {output_file}")
    else:
        print(f"No files matching the pattern '{file_pattern}' were found.")


def create_nation_master(service_type: str, state_fips: str, counties: list):
    folder_path = f'../../../results/ookla/US/cbg/raw_census/'
    output_folder = f'../../../results/ookla/US/cbg/raw_masters/'
    nation_file = '../../../datasets/census/US/regions/woodard_countywise_california_fips.csv'
    
    nation_df = pd.read_csv(nation_file)
    nation_mapping = nation_df.set_index("COUNTY_FIPS")["WOODARD NATION NAME"].to_dict()

    # print(nation_mapping)

    # print("Keys in nation_mapping:")
    # print(nation_mapping.keys())    
    
    nation_data = {}

    for county_fips in counties:
        file_pattern = f'ookla_{service_type}_cbg_{state_fips}_{county_fips}'
        
        for file_name in os.listdir(folder_path):
            if file_pattern in file_name:
                file_path = os.path.join(folder_path, file_name)
                df = pd.read_csv(file_path)

                # print(file_path)

                county_fips = int(county_fips) 
                nation_name = nation_mapping.get(county_fips)
                # print(nation_name)

                if nation_name:
                    if nation_name not in nation_data:
                        nation_data[nation_name] = []
                    nation_data[nation_name].append(df)

    for nation_name, data_frames in nation_data.items():
        if data_frames:
            master_df = pd.concat(data_frames, ignore_index=True)
            output_file = os.path.join(output_folder, f'nation_master_{service_type}_{state_fips}_{nation_name}.csv')
            master_df.to_csv(output_file, index=False)
            print(f"Master file for {nation_name} created: {output_file}")
        else:
            print(f"No data found for nation: {nation_name}")
