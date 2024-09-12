from datetime import datetime
import geopandas as gpd
import pandas as pd

def quarter_start(year: int, q: int) -> datetime:
    if not 1 <= q <= 4:
        raise ValueError("Quarter must be within [1, 2, 3, 4]")
    
    month = [1, 4, 7, 10]
    return datetime(year, month[q - 1], 1)

def get_tile_url(service_type: str, year: int, q: int) -> str:
    dt = quarter_start(year, q)
    
    base_url = "https://ookla-open-data.s3-us-west-2.amazonaws.com/shapefiles/performance"
    url = f"{base_url}/type%3D{service_type}/year%3D{dt:%Y}/quarter%3D{q}/{dt:%Y-%m-%d}_performance_{service_type}_tiles.zip"
    return url

def ookla_county_at_cbg(service_type: str, state_fips: str, county_fips: str, year: int):

    all_tiles_in_county_block_groups = pd.DataFrame()
    
    print('Downloading ookla data...')
    output_file = f"../../../datasets/ookla/US/cbg/raw/ookla_fixed_cbg_{state_fips}_{county_fips}_raw.csv"

    # Construct the block group URL using the state FIPS code
    block_group_url = f"https://www2.census.gov/geo/tiger/TIGER{year}/BG/tl_{year}_{state_fips}_bg.zip"
    # print(block_group_url)

    block_groups = gpd.read_file(block_group_url)

    # Filter block groups by state and county FIPS code
    county_block_groups = block_groups.loc[(block_groups['STATEFP'] == state_fips) & (block_groups['COUNTYFP'] == county_fips)]

    # Iterate over all four quarters
    for quarter in range(1, 5):
        
        print(f'Quarter = {quarter}')
        
        tile_url = get_tile_url(service_type, year, quarter)
        # print(f'Tile URL = {tile_url}')

        tiles = gpd.read_file(tile_url)

        # Reproject county block groups to match the tiles CRS
        county_block_groups = county_block_groups.to_crs(tiles.crs)

        # Perform spatial join to find tiles within county block groups for the current quarter
        tiles_in_county_block_groups = gpd.sjoin(tiles, county_block_groups, how="inner", predicate='intersects')

        # Convert to Mbps for easier reading
        tiles_in_county_block_groups['avg_d_mbps'] = tiles_in_county_block_groups['avg_d_kbps'] / 1000
        tiles_in_county_block_groups['avg_u_mbps'] = tiles_in_county_block_groups['avg_u_kbps'] / 1000

        # Add year and quarter columns
        tiles_in_county_block_groups['year'] = year
        tiles_in_county_block_groups['quarter'] = quarter

        # Concatenate the current quarter's results with the previous quarters
        all_tiles_in_county_block_groups = pd.concat([all_tiles_in_county_block_groups, tiles_in_county_block_groups])

    # Save the final concatenated result to a CSV file
    all_tiles_in_county_block_groups.to_csv(output_file, index=False)
    print(f'Download complete and saved in {output_file}')


def combine_same_cbg_rows(state_fips: str, county_fips: str):
    print('Combining same cbg rows...')
    input_csv = f"../../../datasets/ookla/US/cbg/raw/ookla_fixed_cbg_{state_fips}_{county_fips}_raw.csv"
    output_file = f"../../../datasets/ookla/US/cbg/clean/ookla_fixed_cbg_{state_fips}_{county_fips}.csv"

    df = pd.read_csv(input_csv)

    grouped_df = df.groupby('GEOID').agg({
        'avg_d_mbps': ['mean', 'median'],
        'avg_u_mbps': ['mean', 'median'],
        'avg_lat_ms': ['mean', 'median'],
        'tests'     : 'sum',
        'devices'   : 'sum'
    }).reset_index()

    # Flatten the multi-level columns resulting from the aggregation
    grouped_df.columns = ['_'.join(col).strip() if col[1] else col[0] for col in grouped_df.columns.values]

    # Rename columns for clarity
    grouped_df.rename(columns={
        'tests_sum': 'total_tests',
        'devices_sum': 'total_devices'
    }, inplace=True)

    # Merge the non-aggregated columns
    non_agg_columns = df[['GEOID', 'year', 'STATEFP', 'COUNTYFP', 'TRACTCE', 'BLKGRPCE', 'ALAND']].drop_duplicates(subset=['GEOID'])
    final_df = pd.merge(non_agg_columns, grouped_df, on='GEOID')

    subset_columns_df = final_df[['GEOID','year','STATEFP', 'COUNTYFP', 'TRACTCE', 'BLKGRPCE','ALAND', 'avg_d_mbps_mean', 'avg_d_mbps_median', 'avg_u_mbps_mean', 'avg_u_mbps_median', 'avg_lat_ms_mean', 'avg_lat_ms_median', 'total_tests', 'total_devices']]

    # remove sorting if needed
    subset_columns_df = subset_columns_df.sort_values(by='GEOID')

    subset_columns_df.to_csv(output_file, index=False)
    print(f'Aggregated data saved to {output_file}.')
