import os
import pandas as pd

files = [
    '../../results/mlab/US/Yearly Masters/2020_US_state_county_census.csv',
    '../../results/mlab/US/Yearly Masters/2021_US_state_county_census.csv',
    '../../results/mlab/US/Yearly Masters/2022_US_state_county_census.csv',
    '../../results/mlab/US/Yearly Masters/2023_US_state_county_census.csv',
    '../../results/mlab/US/Yearly Masters/2024_US_state_county_census.csv'
]

combined_data = pd.DataFrame()

for file in files:
    df = pd.read_csv(file)
    combined_data = combined_data.append(df, ignore_index=True)

combined_data.to_csv('../../results/mlab/US/Yearly Masters/combined_data.csv', index=False)

