# Get ookla and census data at CBG level for any county

"""
California      06
---
Alameda         001
Contra Costa    013 
Marin           041
Napa            055
San Mateo       081
Santa Clara     085
Solano          095
Sonoma          097
San Francisco   075
---
Yolo            113 - done
"""

from get_measurement_data import ookla_county_at_cbg, combine_same_cbg_rows
from get_census_data import clean_gender_age, add_gender_age_density, add_bg_shape, add_income, add_education, add_race
from file_functions import create_master_file

year =  2023
service_type = 'fixed'

state = '48'
counties = ['497','349','363']

for county in counties:
    print(f'Processing for {county}----------')
    ookla_county_at_cbg(service_type, state, county, year)

    # combine_same_cbg_rows(state, county)

#     add_gender_age_density(state, county)

#     add_income(state, county)

#     add_education(state, county)

#     add_race(state, county)

#     add_bg_shape(state, county, year)

# create_master_file(service_type, state)