# Get ookla and census data at CBG level for any county

from get_measurement_data import ookla_county_at_cbg, combine_same_cbg_rows, clean_headers
from get_census_data import add_gender_age_density, add_bg_shape, add_income, add_education, add_race
from file_functions import create_master_file, create_state_master, create_nation_master

import pandas as pd

year =  2023
service_type = 'fixed'

# # test_county = 'yolo'
# state = '06'
# counties = ['113']

# # bay area - the left coast
# state = '06'
# counties = ['001','013', '041','055','081','085', '095', '097','075']

# # middlecalifornia area - the far west
# state = '06'
# counties = ['025', '037', '059', '065', '073', '079', '083', '111']

# # losangeles area - el norte
# state = '06'
# counties = ['019', '029', '031', '039', '043', '047', '099', '107']

# # dallas area - greaster appalachia
# state = '48'
# counties = ['085', '097', '113', '121', '139', '143', '147', '181', '221', '231', '251', '257', '349', '363', '367', '397', '425', '439', '497']

# # houston area - deep south (CONFIRM ALL COUNTIES)
# state = '48'
# counties = ['015', '039', '071', '157', '167', '201', '291', '339', '473']

# # south texas area - el norte
# state = '48'
# counties = ['479', '463', '507', '127', '325', '163', '283', '131', '311', '297']

# Texas has a set of counties in Midlands too! (CONSIDER)

# TO DO: (trying below) instead of this list, read from the csv file I have created, and default it to a state or even an area 

# rest of California:
state = '06'
# counties = ['003', '005', '007', '009', '011', '015', '017', '021', '023', '027', '033', '035', '045', '049', '051', '053', '057', '061', '063', '067', '069', '071']
# counties = ['077', '087', '089', '091', '093', '101', '103', '105', '109', '113', '115']

#all of california
counties = ['001','013', '041','055','081','085', '095', '097','075', '025', '037', '059', '065', '073', '079', '083', '111', '019', '029', '031', '039', '043', '047', '099', '107', '003', '005', '007', '009', '011', '015', '017', '021', '023', '027', '033', '035', '045', '049', '051', '053', '057', '061', '063', '067', '069', '071', '077', '087', '089', '091', '093', '101', '103', '105', '109', '113', '115']

# for county in counties:
#     print(f'Processing for {county}----------')
    
#     # ookla_county_at_cbg(service_type, state, county, year)

#     # combine rows OR clean headers only
#     # combine_same_cbg_rows(state, county)
#     clean_headers(state, county)

#     add_gender_age_density(state, county)

#     add_income(state, county)

#     add_education(state, county)

#     add_race(state, county)

    # do I need bg_shape of the CBG when I now have multiple rows for each CBG in my data? this is used only for
    # tableau, and I don't know if I can still put this on tableau. CAN I? (repeated spatial data)
    # since I am now capturing the ookla spatial data as well (where the test was taken), I think I can plot 
    # my required graphs using that.
    # ignoring this for now since I can always come back and add this.

    # add_bg_shape(state, county, year)

# create_master_file(service_type, state, counties, region)
# create_state_master(service_type, state)
create_nation_master(service_type, state, counties)

#test