import pandas as pd

df_source = pd.read_csv("../../../results/mlab/US/Woodard_research/mlab_woodard_race_gender.csv")

# Filter data to include rows of 2023
df = df_source[(df_source['year'] == 2023)]

def find_metrics(df):
    print(df.shape[0])
    print(df['median_household_income'].mean())
    print(df['median_household_income'].std() / df['median_household_income'].mean() * 100)
    print(df['download_avg'].mean())
    print(df['upload_avg'].mean())
    print(df['download_max'].mean())
    print(df['upload_max'].mean())
    print(df['download_min'].mean())
    print(df['upload_min'].mean())
    
# print("\nNational Average - Total Population:\n")
find_metrics(df)

# genders
# df_majority_male = df[(df['percentage_male'] > 50)]
# print("\nFor counties with majority male population:\n")
# find_metrics(df_majority_male)

# df_majority_female = df[(df['percentage_female'] > 50)]
# print("\nFor counties with majority female population:\n")
# find_metrics(df_majority_female)

# races
# white
# df_white_majority = df[(df['percentage_white'] > 50)]
# find_metrics(df_white_majority)

# df_white_more_than_90 = df[(df['percentage_white'] >= 90)]
# find_metrics(df_white_more_than_90)

# df_white_less_than_10 = df[(df['percentage_white'] <= 10)]
# find_metrics(df_white_less_than_10)

# black
# df_black_majority = df[(df['percentage_black_or_african'] > 50)]
# find_metrics(df_black_majority)

# df_black_more_than_80 = df[(df['percentage_black_or_african'] >= 80)]
# find_metrics(df_black_more_than_80)

# df_black_less_than_10 = df[(df['percentage_black_or_african'] <= 10)]
# find_metrics(df_black_less_than_10)

# american indian or alaskan
# df_american_indian_majority = df[(df['percentage_american_indian_and_native_alaskan'] > 50)]
# find_metrics(df_american_indian_majority)

# df_american_indian_more_than_80 = df[(df['percentage_american_indian_and_native_alaskan'] >= 80)]
# find_metrics(df_american_indian_more_than_80)

# df_american_indian_less_than_10 = df[(df['percentage_american_indian_and_native_alaskan'] <= 10)]
# find_metrics(df_american_indian_less_than_10)

# asian
# df_asian_majority = df[(df['percentage_asian'] > 50)]
# find_metrics(df_asian_majority)

# df_asian_more_than_80 = df[(df['percentage_asian'] >= 80)]
# find_metrics(df_asian_more_than_80)

# df_asian_less_than_10 = df[(df['percentage_asian'] <= 10)]
# find_metrics(df_asian_less_than_10)

# native hawaiian
# df_native_hawaiian_majority = df[(df['percentage_native_hawaiian_and_other_pacific_islander'] > 50)]
# find_metrics(df_native_hawaiian_majority)

# df_native_hawaiian_more_than_80 = df[(df['percentage_native_hawaiian_and_other_pacific_islander'] >= 80)]
# find_metrics(df_native_hawaiian_more_than_80)

# df_native_hawaiian_less_than_10 = df[(df['percentage_native_hawaiian_and_other_pacific_islander'] <= 10)]
# find_metrics(df_native_hawaiian_less_than_10)

# two or more races
# df_two_majority = df[(df['percentage_two_or_more_races'] > 50)]
# find_metrics(df_two_majority)

# df_two_more_than_80 = df[(df['percentage_two_or_more_races'] >= 80)]
# find_metrics(df_two_more_than_80)

# df_two_less_than_10 = df[(df['percentage_two_or_more_races'] <= 10)]
# find_metrics(df_two_less_than_10)

# hispanic
# df_hispanic_majority = df[(df['percentage_hispanic'] > 50)]
# find_metrics(df_hispanic_majority)

# df_hispanic_more_than_80 = df[(df['percentage_hispanic'] >= 80)]
# find_metrics(df_hispanic_more_than_80)

# df_hispanic_less_than_10 = df[(df['percentage_hispanic'] <= 10)]
# find_metrics(df_hispanic_less_than_10)
