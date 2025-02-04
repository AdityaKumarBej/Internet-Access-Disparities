import pandas as pd

df = pd.read_csv("../../../results/ookla/US/cbg/census/ookla_fixed_cbg_06_001_census.csv")

unwanted_columns = ['less_than_high_school_diploma_y', 'high_school_diploma_only_y', 'bachelor_or_associate_degree_y', 'masters_or_more_y']
df = df.drop(columns=unwanted_columns)

df.to_csv("../../../results/ookla/US/cbg/census/ookla_fixed_cbg_06_001_census.csv", index=False)