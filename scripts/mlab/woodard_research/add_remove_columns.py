import pandas as pd

df = pd.read_csv("../../../results/mlab/US/Woodard_research/mlab_woodard_race_gender_age.csv")

df['percentage_asian_pacific_american'] = df['percentage_asian'] + df['percentage_native_hawaiian_and_other_pacific_islander']

# 'total_white','total_black_or_african','total_american_indian_and_native_alaskan','total_asian','total_native_hawaiian_and_other_pacific_islander','total_two_or_more_races','total_hispanic'
unwanted_columns = ['percentage_asian', 'percentage_native_hawaiian_and_other_pacific_islander']
df = df.drop(columns=unwanted_columns)

df.to_csv("../../../results/mlab/US/Woodard_research/mlab_woodard_race_gender_age_new.csv", index=False)