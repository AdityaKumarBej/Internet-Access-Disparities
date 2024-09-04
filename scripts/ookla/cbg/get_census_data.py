import pandas as pd
import geopandas as gpd

def transform_geoid(geoid):
        # Take stuff only after 'US'
        geoid = geoid.split('US')[1]
        # Remove preceding zeroes
        geoid = geoid.lstrip('0')
        return geoid

def clean_gender_age(state_fips: str, county_fips: str):
    print('Cleaning gender and age dataset...')
    input_census_csv = f"../../../datasets/census/US/cbg/gender_age/raw/{state_fips}_{county_fips}.csv"
    output_census_csv = f"../../../datasets/census/US/cbg/gender_age/clean/{state_fips}_{county_fips}.csv"

    df = pd.read_csv(input_census_csv)

    # Apply the transformation to the GEOID column
    df['GEOID']             = df['geoid'].apply(transform_geoid)

    df['total_population']  = df['B01001001']

    df['total_male']        = df['B01001002']
    df['total_female']      = df['B01001026']
    df['percentage_male']   = df['total_male']  /df['total_population'] * 100
    df['percentage_female'] = df['total_female']/df['total_population'] * 100

    # Section 1: Percentage Age Under 5
    df['percentage_age_under_5'] = (df['B01001003'] + df['B01001027']) / df['total_population'] * 100

    # Section 2: Percentage Age 5-17
    df['percentage_age_5_17'] = (df['B01001004'] + df['B01001005'] + df['B01001006'] +
                                df['B01001028'] + df['B01001029'] + df['B01001030']) / df['total_population'] * 100

    # Section 3: Percentage Age 18-64 (add the relevant columns)
    df['percentage_age_18_64'] = (df['B01001007'] + df['B01001008'] + df['B01001009'] +
                                df['B01001010'] + df['B01001011'] + df['B01001012'] +
                                df['B01001013'] + df['B01001014'] + df['B01001015'] +
                                df['B01001016'] + df['B01001017'] + df['B01001018'] +
                                df['B01001019'] + df['B01001031'] + df['B01001032'] + 
                                df['B01001033'] + df['B01001034'] + df['B01001035'] + 
                                df['B01001036'] + df['B01001037'] + df['B01001038'] + 
                                df['B01001039'] + df['B01001040'] + df['B01001041'] + 
                                df['B01001042'] + df['B01001043']) / df['total_population'] * 100

    # Section 4: Percentage Age Over 65 (add the relevant columns)
    df['percentage_age_over_65'] = (df['B01001020'] + df['B01001021'] + df['B01001022'] + 
                                    df['B01001023'] + df['B01001024'] + df['B01001025'] + 
                                    df['B01001044'] + df['B01001045'] + df['B01001046'] + 
                                    df['B01001047'] + df['B01001048'] + df['B01001049']) / df['total_population'] * 100

    subset_df = df[['GEOID', 'name', 'total_population', 'percentage_male', 'percentage_female', 'percentage_age_under_5', 'percentage_age_5_17', 'percentage_age_18_64', 'percentage_age_over_65']]

    subset_df.to_csv(output_census_csv)
    print(f'Clean dataset saved in {output_census_csv}.')

def add_gender_age_density(state_fips: str, county_fips: str):

    clean_gender_age(state_fips, county_fips)
    
    print('Adding gender and age data to measurement file...')
    ookla_csv = f"../../../results/ookla/US/cbg/clean/ookla_fixed_cbg_{state_fips}_{county_fips}.csv"
    census_csv = f"../../../datasets/census/US/cbg/gender_age/clean/{state_fips}_{county_fips}.csv" 
    ookla_df = pd.read_csv(ookla_csv)
    census_df = pd.read_csv(census_csv)

    merged_df = pd.merge(ookla_df, census_df[['GEOID', 'name', 'total_population', 'percentage_male', 'percentage_female', 'percentage_age_under_5', 'percentage_age_5_17', 'percentage_age_18_64', 'percentage_age_over_65']], on='GEOID', how='left')

    # add population density
    merged_df['land_area'] = merged_df['ALAND'] / 1000000
    merged_df['population_density'] = merged_df['total_population'] / merged_df['land_area']

    output_csv = f"../../../results/ookla/US/cbg/census/ookla_fixed_cbg_{state_fips}_{county_fips}_census.csv"

    merged_df.to_csv(output_csv, index=False)
    print(f'Complete and saved in {output_csv}.')

def add_bg_shape(state_fips: str, county_fips: str, year: int):
    print('Adding block group shape columns to census file...')
    block_group_url = f"https://www2.census.gov/geo/tiger/TIGER{year}/BG/tl_{year}_{state_fips}_bg.zip"

    base_file = f"../../../results/ookla/US/cbg/census/ookla_fixed_cbg_{state_fips}_{county_fips}_census.csv"

    shape_df = gpd.read_file(block_group_url)
    base_df = pd.read_csv(base_file)

    shape_df['GEOID'] = shape_df['GEOID'].str.lstrip('0')
    base_df['GEOID'] = base_df['GEOID'].astype(str)

    merged_df = pd.merge(base_df, shape_df[['GEOID', 'INTPTLAT', 'INTPTLON', 'geometry']], on='GEOID', how='left')

    merged_df = merged_df.rename(columns={'INTPTLAT': 'latitude', 'INTPTLON': 'longitude'})

    merged_df.to_csv(base_file, index=False)
    print(f'File saved in {base_file}')

def add_income(state_fips: str, county_fips: str):
    print('Adding income data to census file...')
    base_csv = f"../../../results/ookla/US/cbg/census/ookla_fixed_cbg_{state_fips}_{county_fips}_census.csv"
    income_csv = f"../../../datasets/census/US/cbg/income/{state_fips}_{county_fips}.csv" 

    base_df = pd.read_csv(base_csv)
    income_df = pd.read_csv(income_csv)

    income_df['GEOID'] = income_df['geoid'].apply(transform_geoid)

    income_df = income_df.rename(columns={'B19013001': 'median_household_income'})

    base_df['GEOID'] = base_df['GEOID'].astype(str)
    income_df['GEOID'] = income_df['GEOID'].astype(str)

    merged_df = pd.merge(base_df, income_df[['GEOID', 'median_household_income']], on='GEOID', how='left')

    merged_df.to_csv(base_csv, index=False)
    print(f'File saved in {base_csv}')

def add_education(state_fips: str, county_fips: str):
    print('Adding education data to census file...')
    base_csv = f"../../../results/ookla/US/cbg/census/ookla_fixed_cbg_{state_fips}_{county_fips}_census.csv"
    edu_csv = f"../../../datasets/census/US/cbg/education/{state_fips}_{county_fips}.csv"

    base_df = pd.read_csv(base_csv)
    edu_df = pd.read_csv(edu_csv)

    edu_df['GEOID'] = edu_df['geoid'].apply(transform_geoid)
    base_df['GEOID'] = base_df['GEOID'].astype(str)
    edu_df['GEOID'] = edu_df['GEOID'].astype(str)

    total = edu_df['B15002001']

    edu_df['total_less_than_high_school_diploma'] = edu_df['B15002003'] + edu_df['B15002004'] + edu_df['B15002005'] + edu_df['B15002006'] + edu_df['B15002007'] + edu_df['B15002008'] + edu_df['B15002009'] + edu_df['B15002010'] + edu_df['B15002020'] + edu_df['B15002021'] + edu_df['B15002022'] + edu_df['B15002023'] + edu_df['B15002024'] + edu_df['B15002025'] + edu_df['B15002026'] + edu_df['B15002027']
    edu_df['total_high_school_diploma_only'] = edu_df['B15002011'] + edu_df['B15002012'] + edu_df['B15002013'] + edu_df['B15002028'] + edu_df['B15002029'] + edu_df['B15002030']
    edu_df['total_bachelor_or_associate_degree'] = edu_df['B15002014'] + edu_df['B15002015'] + edu_df['B15002031'] + edu_df['B15002032']
    edu_df['total_masters_or_more'] = edu_df['B15002016'] + edu_df['B15002017'] + edu_df['B15002018'] + edu_df['B15002033'] + edu_df['B15002034'] + edu_df['B15002035']

    edu_df['less_than_high_school_diploma'] = edu_df['total_less_than_high_school_diploma'] / total * 100
    edu_df['high_school_diploma_only'] = edu_df['total_high_school_diploma_only'] / total * 100
    edu_df['bachelor_or_associate_degree'] = edu_df['total_bachelor_or_associate_degree'] / total * 100
    edu_df['masters_or_more'] = edu_df['total_masters_or_more'] / total * 100


    merged_df = pd.merge(base_df, edu_df[['GEOID', 'less_than_high_school_diploma','high_school_diploma_only', 'bachelor_or_associate_degree', 'masters_or_more' ]], on='GEOID', how='left')

    # output_file = f"../../../results/ookla/USA/cbg/census/ookla_fixed_cbg_{state_fips}_{county_fips}_census_edu.csv"

    merged_df.to_csv(base_csv, index=False)
    print(f'File saved in {base_csv}')

def add_race(state_fips: str, county_fips: str):
    print('Adding race data to census file...')
    base_csv = f"../../../results/ookla/US/cbg/census/ookla_fixed_cbg_{state_fips}_{county_fips}_census.csv"
    race_csv = f"../../../datasets/census/US/cbg/race/{state_fips}_{county_fips}.csv"
    # output_file = f"../../../results/ookla/USA/cbg/census/ookla_fixed_cbg_{state_fips}_{county_fips}_census_race.csv"

    base_df = pd.read_csv(base_csv)
    race_df = pd.read_csv(race_csv)

    race_df['GEOID'] = race_df['geoid'].apply(transform_geoid)
    base_df['GEOID'] = base_df['GEOID'].astype(str)
    race_df['GEOID'] = race_df['GEOID'].astype(str)

    total = race_df['B03002001']

    race_df['hispanic_latino'] = race_df['B03002012'] / total * 100
    race_df['white_alone'] = race_df['B03002003'] / total * 100
    race_df['black_or_african_american_alone'] = race_df['B03002004'] / total * 100
    race_df['american_indian_and_alaskan_native_alone'] = race_df['B03002005'] / total * 100
    race_df['asian_alone'] = race_df['B03002006'] / total * 100
    race_df['native_hawaiian_and_other_pacific_islander_alone'] = race_df['B03002007'] / total * 100
    race_df['some_other_race_alone'] = race_df['B03002008'] / total * 100
    race_df['two_or_more_races'] = (race_df['B03002009']) / total * 100

    merged_df = pd.merge(base_df, race_df[['GEOID', 'hispanic_latino', 'white_alone', 'black_or_african_american_alone', 'american_indian_and_alaskan_native_alone', 'asian_alone', 'native_hawaiian_and_other_pacific_islander_alone', 'some_other_race_alone', 'two_or_more_races']], on='GEOID', how='left')

    merged_df.to_csv(base_csv, index=False)
    print(f'File saved in {base_csv}')