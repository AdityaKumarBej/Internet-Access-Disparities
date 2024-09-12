import pandas as pd
import geopandas as gpd
import requests
from pathlib import Path
import numpy as np

def transform_geoid(geoid):
        # Take stuff only after 'US'
        geoid = geoid.split('US')[1]
        # Remove preceding zeroes
        geoid = geoid.lstrip('0')
        return geoid

def get_gender_age_density(api_key: str, state_fips: str, county_fips: str, table_code: str):

    print(' Downloading gender and age data...')

    url = f"https://api.census.gov/data/2022/acs/acs5?get=NAME,group({table_code})&for=block%20group:*&in=state:{state_fips}%20county:{county_fips}&key={api_key}"

    output_file= f"../../../datasets/census/US/cbg/gender_age/{state_fips}_{county_fips}.csv"

    response = requests.get(url)

    # print(f"Response Status Code: {response.status_code}")
    # print(f"Response Content: {response.text[:1000]}")
    
    if response.status_code == 200:

        data = response.json()

        df = pd.DataFrame(data[1:], columns=data[0])

        df['GEOID']             = df['GEO_ID'].apply(transform_geoid)

        df['total_population']  = pd.to_numeric(df['B01001_001E'], errors='coerce')

        df['total_male']        = pd.to_numeric(df['B01001_002E'], errors='coerce')
        df['total_female']      = pd.to_numeric(df['B01001_026E'], errors='coerce')

        df['percentage_male']   = pd.to_numeric(df['total_male'])  /df['total_population'] * 100
        df['percentage_female'] = pd.to_numeric(df['total_female']) /df['total_population'] * 100

        # Section 1: Percentage Age Under 5
        df['percentage_age_under_5'] = (pd.to_numeric(df['B01001_003E']) + pd.to_numeric(df['B01001_027E'])) / df['total_population'] * 100

        # Section 2: Percentage Age 5-17
        df['percentage_age_5_17'] = (pd.to_numeric(df['B01001_004E']) + pd.to_numeric(df['B01001_005E']) + pd.to_numeric(df['B01001_006E']) + pd.to_numeric(df['B01001_028E']) + pd.to_numeric(df['B01001_029E']) + pd.to_numeric(df['B01001_030E'])) / df['total_population'] * 100

        # Section 3: Percentage Age 18-64 (add the relevant columns)
        df['percentage_age_18_64'] = (pd.to_numeric(df['B01001_007E']) + pd.to_numeric(df['B01001_008E']) + pd.to_numeric(df['B01001_009E']) +
                                    pd.to_numeric(df['B01001_010E']) + pd.to_numeric(df['B01001_011E']) + pd.to_numeric(df['B01001_012E']) +
                                    pd.to_numeric(df['B01001_013E']) + pd.to_numeric(df['B01001_014E']) + pd.to_numeric(df['B01001_015E']) +
                                    pd.to_numeric(df['B01001_016E']) + pd.to_numeric(df['B01001_017E']) + pd.to_numeric(df['B01001_018E']) +
                                    pd.to_numeric(df['B01001_019E']) + pd.to_numeric(df['B01001_031E']) + pd.to_numeric(df['B01001_032E']) + 
                                    pd.to_numeric(df['B01001_033E']) + pd.to_numeric(df['B01001_034E']) + pd.to_numeric(df['B01001_035E']) + 
                                    pd.to_numeric(df['B01001_036E']) + pd.to_numeric(df['B01001_037E']) + pd.to_numeric(df['B01001_038E']) + 
                                    pd.to_numeric(df['B01001_039E']) + pd.to_numeric(df['B01001_040E']) + pd.to_numeric(df['B01001_041E']) + 
                                    pd.to_numeric(df['B01001_042E']) + pd.to_numeric(df['B01001_043E'])) / df['total_population'] * 100

        # Section 4: Percentage Age Over 65 (add the relevant columns)
        df['percentage_age_over_65'] = (pd.to_numeric(df['B01001_020E']) + pd.to_numeric(df['B01001_021E']) + pd.to_numeric(df['B01001_022E']) + 
                                        pd.to_numeric(df['B01001_023E']) + pd.to_numeric(df['B01001_024E']) + pd.to_numeric(df['B01001_025E']) + 
                                        pd.to_numeric(df['B01001_044E']) + pd.to_numeric(df['B01001_045E']) + pd.to_numeric(df['B01001_046E']) + 
                                        pd.to_numeric(df['B01001_047E']) + pd.to_numeric(df['B01001_048E']) + pd.to_numeric(df['B01001_049E'])) / df['total_population'] * 100

        subset_df = df[['GEOID', 'total_population', 'percentage_male', 'percentage_female', 'percentage_age_under_5', 'percentage_age_5_17', 'percentage_age_18_64', 'percentage_age_over_65']]

        subset_df.to_csv(output_file, index=False)

        print(f" Downloaded gender and age data successfully saved to {output_file}")

    else:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")


def add_gender_age_density(state_fips: str, county_fips: str):

    api_key = Path("../../../datasets/census/US/myapikey.txt").read_text().strip()
    table_code = 'B01001'

    get_gender_age_density(api_key, state_fips, county_fips, table_code)
    
    print(' Adding gender and age data to measurement file...')

    census_csv = f"../../../datasets/census/US/cbg/gender_age/{state_fips}_{county_fips}.csv"
    ookla_csv = f"../../../datasets/ookla/US/cbg/clean/ookla_fixed_cbg_{state_fips}_{county_fips}.csv"

    ookla_df = pd.read_csv(ookla_csv)
    census_df = pd.read_csv(census_csv)

    merged_df = pd.merge(ookla_df, census_df, on='GEOID', how='left')

    # add population density
    merged_df['land_area'] = merged_df['ALAND'] / 1000000
    merged_df['population_density'] = merged_df['total_population'] / merged_df['land_area']

    output_csv = f"../../../results/ookla/US/cbg/census/ookla_fixed_cbg_{state_fips}_{county_fips}_census.csv"

    merged_df.to_csv(output_csv, index=False)
    print(f' Complete and saved in {output_csv}.')

def get_income(api_key: str, state_fips: str, county_fips: str, table_code: str):

    print(' Downloading income data...')

    url = f"https://api.census.gov/data/2022/acs/acs5?get=NAME,group({table_code})&for=block%20group:*&in=state:{state_fips}%20county:{county_fips}&key={api_key}"

    output_file= f"../../../datasets/census/US/cbg/income/{state_fips}_{county_fips}.csv"

    response = requests.get(url)
    
    if response.status_code == 200:

        data = response.json()

        df = pd.DataFrame(data[1:], columns=data[0])

        df['GEOID']                     = df['GEO_ID'].apply(transform_geoid)
        df['median_household_income']   = pd.to_numeric(df['B19013_001E'])

        # df['median_household_income'] = df['median_household_income'].apply(lambda x: x if x > 0 else np.nan)

        subset_df = df[['GEOID', 'median_household_income']]

        subset_df.to_csv(output_file, index=False)

        print(f" Downloaded income data successfully saved to {output_file}")

    else:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")

def add_income(state_fips: str, county_fips: str):

    api_key = Path("../../../datasets/census/US/myapikey.txt").read_text().strip()
    table_code = 'B19013'

    get_income(api_key, state_fips, county_fips, table_code)

    print(' Adding income data to census file...')

    base_csv = f"../../../results/ookla/US/cbg/census/ookla_fixed_cbg_{state_fips}_{county_fips}_census.csv"
    income_csv = f"../../../datasets/census/US/cbg/income/{state_fips}_{county_fips}.csv" 

    base_df = pd.read_csv(base_csv)
    income_df = pd.read_csv(income_csv)

    merged_df = pd.merge(base_df, income_df, on='GEOID', how='left')

    merged_df.to_csv(base_csv, index=False)
    print(f' Complete and saved in {base_csv}')

def get_education(api_key: str, state_fips: str, county_fips: str, table_code: str):
    
    print(' Downloading education data...')

    url = f"https://api.census.gov/data/2022/acs/acs5?get=NAME,group({table_code})&for=block%20group:*&in=state:{state_fips}%20county:{county_fips}&key={api_key}"

    output_file= f"../../../datasets/census/US/cbg/education/{state_fips}_{county_fips}.csv"

    response = requests.get(url)
    
    if response.status_code == 200:

        data = response.json()

        df = pd.DataFrame(data[1:], columns=data[0])

        df['GEOID'] = df['GEO_ID'].apply(transform_geoid)

        total = pd.to_numeric(df['B15002_001E'])

        df['less_than_high_school_diploma']   = (pd.to_numeric(df['B15002_003E']) + pd.to_numeric(df['B15002_004E']) + pd.to_numeric(df['B15002_005E']) + pd.to_numeric(df['B15002_006E']) + pd.to_numeric(df['B15002_007E']) + pd.to_numeric(df['B15002_008E']) + pd.to_numeric(df['B15002_009E']) + pd.to_numeric(df['B15002_010E']) + pd.to_numeric(df['B15002_020E']) + pd.to_numeric(df['B15002_021E']) + pd.to_numeric(df['B15002_022E']) + pd.to_numeric(df['B15002_023E']) + pd.to_numeric(df['B15002_024E']) + pd.to_numeric(df['B15002_025E']) + pd.to_numeric(df['B15002_026E']) + pd.to_numeric(df['B15002_027E'])) / total * 100
        df['high_school_diploma_only']        = (pd.to_numeric(df['B15002_011E']) + pd.to_numeric(df['B15002_012E']) + pd.to_numeric(df['B15002_013E']) + pd.to_numeric(df['B15002_028E']) + pd.to_numeric(df['B15002_029E']) + pd.to_numeric(df['B15002_030E'])) / total * 100
        df['bachelor_or_associate_degree']    = (pd.to_numeric(df['B15002_014E']) + pd.to_numeric(df['B15002_015E']) + pd.to_numeric(df['B15002_031E']) + pd.to_numeric(df['B15002_032E'])) / total * 100
        df['masters_or_more']                 = (pd.to_numeric(df['B15002_016E']) + pd.to_numeric(df['B15002_017E']) + pd.to_numeric(df['B15002_018E']) + pd.to_numeric(df['B15002_033E']) + pd.to_numeric(df['B15002_034E']) + pd.to_numeric(df['B15002_035E'])) / total * 100

        subset_df = df[['GEOID', 'less_than_high_school_diploma', 'high_school_diploma_only', 'bachelor_or_associate_degree', 'masters_or_more']]

        subset_df.to_csv(output_file, index=False)

        print(f" Downloaded education data successfully saved to {output_file}")

    else:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")

def add_education(state_fips: str, county_fips: str):

    api_key = Path("../../../datasets/census/US/myapikey.txt").read_text().strip()
    table_code = 'B15002'

    get_education(api_key, state_fips, county_fips, table_code)

    print(' Adding education data to census file...')
    base_csv = f"../../../results/ookla/US/cbg/census/ookla_fixed_cbg_{state_fips}_{county_fips}_census.csv"
    edu_csv = f"../../../datasets/census/US/cbg/education/{state_fips}_{county_fips}.csv"

    base_df = pd.read_csv(base_csv)
    edu_df = pd.read_csv(edu_csv)

    merged_df = pd.merge(base_df, edu_df, on='GEOID', how='left')

    merged_df.to_csv(base_csv, index=False)
    print(f' Complete and saved in {base_csv}')

def get_race(api_key: str, state_fips: str, county_fips: str, table_code: str):
    
    print(' Downloading race data...')

    url = f"https://api.census.gov/data/2022/acs/acs5?get=NAME,group({table_code})&for=block%20group:*&in=state:{state_fips}%20county:{county_fips}&key={api_key}"

    output_file= f"../../../datasets/census/US/cbg/race/{state_fips}_{county_fips}.csv"

    response = requests.get(url)
    
    if response.status_code == 200:

        data = response.json()

        df = pd.DataFrame(data[1:], columns=data[0])

        df['GEOID'] = df['GEO_ID'].apply(transform_geoid)

        total = pd.to_numeric(df['B03002_001E'])

        df['hispanic_latino']                                   = pd.to_numeric(df['B03002_012E']) / total * 100
        df['white_alone']                                       = pd.to_numeric(df['B03002_003E']) / total * 100
        df['black_or_african_american_alone']                   = pd.to_numeric(df['B03002_004E']) / total * 100
        df['american_indian_and_alaskan_native_alone']          = pd.to_numeric(df['B03002_005E']) / total * 100
        df['asian_alone']                                       = pd.to_numeric(df['B03002_006E']) / total * 100
        df['native_hawaiian_and_other_pacific_islander_alone']  = pd.to_numeric(df['B03002_007E']) / total * 100
        df['some_other_race_alone']                             = pd.to_numeric(df['B03002_008E']) / total * 100
        df['two_or_more_races']                                 = pd.to_numeric(df['B03002_009E']) / total * 100
        
        subset_df = df[['GEOID', 'hispanic_latino', 'white_alone', 'black_or_african_american_alone', 'american_indian_and_alaskan_native_alone', 'asian_alone', 'native_hawaiian_and_other_pacific_islander_alone', 'some_other_race_alone', 'two_or_more_races']]

        subset_df.to_csv(output_file, index=False)

        print(f" Downloaded race data successfully saved to {output_file}")

    else:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")

def add_race(state_fips: str, county_fips: str):

    api_key = Path("../../../datasets/census/US/myapikey.txt").read_text().strip()
    table_code = 'B03002'

    get_race(api_key, state_fips, county_fips, table_code)

    print(' Adding race data to census file...')
    base_csv = f"../../../results/ookla/US/cbg/census/ookla_fixed_cbg_{state_fips}_{county_fips}_census.csv"
    race_csv = f"../../../datasets/census/US/cbg/race/{state_fips}_{county_fips}.csv"

    base_df = pd.read_csv(base_csv)
    race_df = pd.read_csv(race_csv)

    merged_df = pd.merge(base_df, race_df, on='GEOID', how='left')

    merged_df.to_csv(base_csv, index=False)
    print(f' Complete and saved in {base_csv}')

def add_bg_shape(state_fips: str, county_fips: str, year: int):

    print(' Adding block group shape columns to census file...')

    # block_group_url = f"https://www2.census.gov/geo/tiger/TIGER{year}/BG/tl_{year}_{state_fips}_bg.zip"
    block_group_file = f"../../../datasets/census/US/cbg/regions/tl_{year}_{state_fips}_bg.zip"
    base_file = f"../../../results/ookla/US/cbg/census/ookla_fixed_cbg_{state_fips}_{county_fips}_census.csv"

    # shape_df = gpd.read_file(block_group_url)
    shape_df = gpd.read_file(block_group_file)
    base_df = pd.read_csv(base_file)

    shape_df['GEOID'] = shape_df['GEOID'].str.lstrip('0')
    base_df['GEOID'] = base_df['GEOID'].astype(str)

    merged_df = pd.merge(base_df, shape_df[['GEOID', 'INTPTLAT', 'INTPTLON', 'geometry']], on='GEOID', how='left')

    merged_df = merged_df.rename(columns={'INTPTLAT': 'latitude', 'INTPTLON': 'longitude'})

    merged_df.to_csv(base_file, index=False)
    print(f' Complete and saved in {base_file}')