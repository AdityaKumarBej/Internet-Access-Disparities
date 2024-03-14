import geopandas as gp
import pandas as pd

county_url = "https://www2.census.gov/geo/tiger/TIGER2023/COUNTY/tl_2023_us_county.zip" 

counties = gp.read_file(county_url)
al_counties = counties.loc[counties['STATEFP'] == '01'].to_crs(4326)
al_counties = al_counties.to_crs(epsg=4326)
print(al_counties.head())
print("-------------------------------------")
CSV_FILE_PATH = "/Users/beja/Desktop/Classes/Winter'24/project/Internet-Access-Disparities/results/ookla/USA/Alabama-01/2023/2023_average_stats.csv"
csv_data = pd.read_csv(CSV_FILE_PATH)

csv_data['GEOID'] = csv_data['GEOID'].astype(str).apply(lambda x: x.zfill(5))

# Merge the GeoDataFrame with the CSV data on the GEOID
merged_data = csv_data.merge(al_counties[['GEOID', 'geometry']], on='GEOID', how='left')

# Convert the pandas DataFrame back to a GeoDataFrame
# This is necessary to retain the geometry column as spatial data
merged_geo_df = gp.GeoDataFrame(merged_data, geometry='geometry', crs="EPSG:4326")

# Checking the first few rows to ensure the merge was successful
print(merged_geo_df.head())

merged_geo_df.to_csv("/Users/beja/Desktop/Classes/Winter'24/project/Internet-Access-Disparities/results/ookla/USA/Alabama-01/2023/merged_data.csv", index=False)