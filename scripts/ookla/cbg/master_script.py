# Get ookla and census data at CBG level for any county

from get_measurement_data import ookla_county_at_cbg, combine_same_cbg_rows
from get_census_data import add_gender_age_density, add_bg_shape, add_income, add_education, add_race
from file_functions import create_master_file

import pandas as pd

year =  2023
service_type = 'fixed'

# state = '06'
# counties = ['113']

# state = '06'
# counties = ['001','013', '041','055','081','085', '095', '097','075', '025', '037', '059', '065', '073', '079', '083', '111', '019', '029', '031', '039', '043', '047', '099', '107']

# state = '48'
# counties = ['085', '097', '113', '121', '139', '143', '147', '181', '221', '231', '251', '257', '349', '363', '367', '397', '425', '439', '497']

# TO DO: (trying below) instead of this list, read from the csv file I have created, and default it to a state or even an area 

# for county in counties:
#     print(f'Processing for {county}----------')
    # ookla_county_at_cbg(service_type, state, county, year)

    # combine_same_cbg_rows(state, county)

    # add_gender_age_density(state, county)

    # add_income(state, county)

    # add_education(state, county)

    # add_race(state, county)

    # add_bg_shape(state, county, year)


my_cbgs = f"../../../datasets/census/US/cbg/regions/cbg_counties.csv"
df = pd.read_csv(my_cbgs)

state_code = '48'
region = 'Dallas Area'

# filtered_df = df[(df['state_code'] == state_code) & (df['region'] == region)]

# counties = filtered_df['county_code'].tolist()

# print(counties)

counties = ['085', '097', '113', '121', '139', '143', '147', '181', '221', '231', '251', '257', '349', '363', '367', '397', '425', '439', '497']

create_master_file(service_type, state_code, counties, region)