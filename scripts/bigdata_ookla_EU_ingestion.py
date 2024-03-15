import pandas as pd
import geopandas as gpd
import os
from pathlib import Path
import numpy as np

# Ensure the required directories exist
data_dir = Path("data")
raw_data_dir = data_dir / "raw_data"
raw_data_dir.mkdir(parents=True, exist_ok=True)

# Definitions for years, quarters, and geographical levels
years = [2019, 2020, 2021, 2022]
quarters = [1, 2, 3, 4]
levels = ["lau", "nuts_3", "nuts_2", "nuts_0"]

# Function to read geometries (assuming you have equivalent GeoJSON or shapefiles)
def read_geometries(level):
    # Replace 'path_to_geometries' with the path to your geometries
    path_to_geometries = f"geometries/{level}.geojson"
    geometries = gpd.read_file(path_to_geometries)
    geometries = geometries.rename(columns={"GISCO_ID": "id", "LAU_NAME": "name"}) if level == "lau" else geometries.rename(columns={"NUTS_ID": "id", "NAME_LATN": "name"})
    return geometries[['id', 'name']]

# Main loop to process data
for year in years:
    for quarter in quarters:
        raw_data_path = raw_data_dir / f"{year}_{quarter}.csv"
        
        # Example assumes you've manually downloaded and named the files accordingly
        if not raw_data_path.exists():
            print(f"Data for {year} Q{quarter} not found. Please download and place it in {raw_data_path}.")
            continue
        
        df = pd.read_csv(raw_data_path)
        
        for level in levels:
            output_dir = data_dir / level
            output_dir.mkdir(exist_ok=True)
            
            geometries = read_geometries(level)
            
            # Join data with geometries (assuming 'df' is a DataFrame with the raw data)
            # This part will depend on the structure of your data and may require spatial joins if your data includes coordinates
            # For simplicity, this example assumes a non-spatial join which would likely be replaced with a spatial operation using geopandas
            joined = pd.merge(df, geometries, on="id", how="inner")
            
            # Perform calculations and save the output
            # Replace 'avg_d_kbps', 'avg_u_kbps', 'avg_lat_ms', 'tests' with your actual column names
            # This section will need to be adjusted based on the actual analysis you wish to perform
            grouped = joined.groupby(['id', 'name']).apply(lambda x: pd.Series({
                'avg_d': np.round(np.average(x['avg_d_kbps'], weights=x['tests']) / 1000, 2),
                'avg_u': np.round(np.average(x['avg_u_kbps'], weights=x['tests']) / 1000, 2),
                'avg_l': np.round(np.average(x['avg_lat_ms'], weights=x['tests']), 2),
                'quarter': f"{year} Q{quarter}"
            })).reset_index()
            
            output_path = output_dir / f"{level}_{year}_{quarter}.csv"
            grouped.to_csv(output_path, index=False)
            print(f"Saved output to {output_path}")

# Assuming you have the data in the format required, this script will need adjustments to fit your actual data schema
