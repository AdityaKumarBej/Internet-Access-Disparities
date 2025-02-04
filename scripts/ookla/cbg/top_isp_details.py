import os
import pandas as pd
import geopandas as gpd

folder_path = "../../../datasets/ISP/newyork"

consolidated_df = pd.DataFrame()

for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    
    if os.path.isfile(file_path):

        # df = pd.read_csv(file_path, low_memory=False)

        df = pd.read_csv(file_path, dtype={'block_geoid': str}, low_memory=False)
        
        #  take a particular provider (say AT&T, verizon, t-mobile...)
        filtered_df = df[df['provider_id'] == 130077].copy() 
        
        # extract geoid
        filtered_df['block_geoid_new'] = filtered_df['block_geoid'].str[:12]

        # print(filtered_df['block_geoid_new'])
        
        # drop duplicates for the same geoid - combine all the lower level rows till cbg
        filtered_df = filtered_df.drop_duplicates(subset=['block_geoid_new'])
        
        consolidated_df = pd.concat([consolidated_df, filtered_df], ignore_index=True)

grouped_df = consolidated_df.groupby(
    ['block_geoid_new', 'provider_id', 'technology']
).size().reset_index(name='count')

output_df = grouped_df[['block_geoid_new', 'provider_id', 'technology']]

technology_details = {  0: 'Other', 
                        10: 'Copper', 
                        40: 'Cable', 
                        50: 'Fiber to the Premises', 
                        60: 'GSO Satellite', 
                        61: 'NGSO Satellite', 
                        70: 'Unlicensed Fixed Wireless', 
                        71: 'Licensed Fixed Wireless', 
                        72: 'LBR Fixed Wireless'
                    }
                        
output_df['technology_name'] = output_df['technology'].map(technology_details)

# add geo spatial data for plotting:
year = 2023
state_fips = '36'
block_group_file = f"../../../datasets/census/US/cbg/regions/tl_{year}_{state_fips}_bg.zip"

shape_df = gpd.read_file(block_group_file)

# print(shape_df)
# shape_df.to_csv('shape.csv', index=False)

shape_df['GEOID'] = shape_df['GEOID'].str.lstrip('0')
output_df['GEOID'] = output_df['block_geoid_new'].astype(str)

merged_df = pd.merge(output_df, shape_df[['GEOID', 'INTPTLAT', 'INTPTLON', 'geometry']], on='GEOID', how='left')

merged_df = merged_df.rename(columns={'INTPTLAT': 'latitude', 'INTPTLON': 'longitude'})

output_csv_path = "output.csv"
merged_df.to_csv(output_csv_path, index=False)

print(f"Output CSV created at: {output_csv_path}")
