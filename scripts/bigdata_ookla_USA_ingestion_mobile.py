from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import geopandas as gp
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import pyogrio
import json
import warnings

# Ignore specific future and deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
# Constants
BASE_SHAPEFILE_PATH = "/Users/beja/Desktop/Classes/Winter'24/project/Internet-Access-Disparities/datasets/OOKLA/shapefiles/performance/"
CENSUS_PATH_TEMPLATE = "/Users/beja/Desktop/Classes/Winter'24/project/Internet-Access-Disparities/datasets/CENSUS/USA/tl_{}_us_county.zip"
BASE_RESULTS_FOLDER = "/Users/beja/Desktop/Classes/Winter'24/project/Internet-Access-Disparities/results/ookla/USA"
TYPE = "mobile"
STATE_FIPS_FILE_PATH = "/Users/beja/Desktop/Classes/Winter'24/project/Internet-Access-Disparities/datasets/USA_state_fips.json"

# State FIPS codes mapping
with open(STATE_FIPS_FILE_PATH, "r") as file:
    STATE_FIPS = json.load(file)

def get_shapefile_path(year, quarter, type=TYPE):
    quarter_dates = {
        1: "01-01",
        2: "04-01",
        3: "07-01",
        4: "10-01"
    }
    date_string = f"{quarter_dates[quarter]}_performance_mobile_tiles/gps_mobile_tiles.shp"
    return f"{BASE_SHAPEFILE_PATH}/type={type}/year={year}/quarter={quarter}/{year}-{date_string}"

def get_census_path(year):
    return CENSUS_PATH_TEMPLATE.format(year)

def analyze_and_save_state_data(year, state, county_stats_list, output_path):
    annual_county_stats = pd.concat(county_stats_list, ignore_index=True)

    # Group by GEOID and calculate the mean for the specified columns
    avg_annual_stats = annual_county_stats.groupby(['GEOID', 'NAMELSAD']).mean().reset_index()
    
    output_file_path = os.path.join(output_path, f"{year}_average_stats.csv")
    avg_annual_stats.to_csv(output_file_path, index=False)
    print(f"Saved average annual data for {state} {year} to {output_file_path}")

def analyze_state_data(year, quarter, state):
    shapefile_path = get_shapefile_path(year, quarter)
    census_path = get_census_path(year)
    # print("the shapefiles path is ---- ", shapefile_path)
    # print("the census path is ---- ", census_path)
    fips_code = STATE_FIPS[state]

    # Load data
    tiles = pyogrio.read_dataframe(shapefile_path)
    counties = gp.read_file(census_path)
    state_counties = counties.loc[counties['STATEFP'] == fips_code].to_crs(4326)

    # Analysis
    tiles_in_state_counties = gp.sjoin(tiles, state_counties, how="inner", op='intersects')

    tiles_in_state_counties['avg_d_mbps'] = tiles_in_state_counties['avg_d_kbps'] / 1000
    tiles_in_state_counties['avg_u_mbps'] = tiles_in_state_counties['avg_u_kbps'] / 1000


    county_stats = (
        tiles_in_state_counties.groupby(["GEOID", "NAMELSAD"])
        .apply(
            lambda x: pd.Series({
                "avg_d_mbps_wt": np.average(x["avg_d_mbps"], weights=x["tests"]),
                "avg_u_mbps_wt": np.average(x["avg_u_mbps"], weights=x["tests"]),
                "avg_lat_ms_wt": np.average(x["avg_lat_ms"], weights=x["tests"])
            })
        )
        .reset_index()
        .merge(
            tiles_in_state_counties.groupby(["GEOID", "NAMELSAD"])
            .agg(tests=("tests", "sum"))
            .reset_index(),
            on=["GEOID", "NAMELSAD"],
        )
    )

    # print(f"THE STATE STATS FOR {state} ARE ---- ", county_stats)
    return county_stats
    #for each county_stat, save to csv file in the output_path only after all 4 quarters are done. csv file name - {YEAR}_output.csv

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def process_state_year(state, year):
    output_path = os.path.join(BASE_RESULTS_FOLDER, f"{state}-{STATE_FIPS[state]}", str(year))
    ensure_directory(output_path)
    county_stats_list = []
    for quarter in range(1, 5):
        print("Processing", state, "Year:", year, "Quarter:", quarter)
        county_stats = analyze_state_data(year, quarter, state)
        county_stats_list.append(county_stats)
    analyze_and_save_state_data(year, state, county_stats_list, output_path)

def main():
    with ThreadPoolExecutor(max_workers=8) as executor:
        # Create a list to hold all of the tasks
        future_to_state_year = {
            executor.submit(process_state_year, state, year): (state, year)
            for year in range(2019, 2024)
            for state in STATE_FIPS.keys()
        }
        # Wait for them to complete and handle results or exceptions
        for future in as_completed(future_to_state_year):
            state, year = future_to_state_year[future]
            try:
                future.result()
            except Exception as exc:
                print(f"{state}-{year} generated an exception: {exc}")

if __name__ == "__main__":
    main()
