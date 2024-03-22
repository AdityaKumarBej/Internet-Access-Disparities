import os
import pandas as pd

files = [
    '../../results/ookla/USA/type=mobile/Yearly Masters/2019_master_w_census.csv',
    '../../results/ookla/USA/type=mobile/Yearly Masters/2021_master_w_census.csv',
    '../../results/ookla/USA/type=mobile/Yearly Masters/2021_master_w_census.csv',
    '../../results/ookla/USA/type=mobile/Yearly Masters/2022_master_w_census.csv',
    '../../results/ookla/USA/type=mobile/Yearly Masters/2023_master_w_census.csv'
]

combined_data = pd.DataFrame()

for file in files:
    df = pd.read_csv(file)
    combined_data = combined_data.append(df, ignore_index=True)

combined_data.to_csv('../../results/ookla/USA/type=mobile/2019_2023_master_w_census.csv', index=False)

