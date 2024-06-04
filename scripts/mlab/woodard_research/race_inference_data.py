import pandas as pd

# Load the data
df_source = pd.read_csv("../../../results/mlab/US/Woodard_research/mlab_woodard_race_gender_age.csv")

# Filter data to include rows of 2023
df = df_source[df_source['year'] == 2023].copy()

# Function to calculate metrics
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
    # print(", ".join(df['county'].astype(str)))
    print(df['Percent_of_adults_with_less_than_a_high_school_diploma_2017_21'].mean())
    print(df['Percent_of_adults_with_a_high_school_diploma_only_2017_21'].mean())
    print(df['Percent_of_adults_completing_some_college_or_associate_degree_2017_21'].mean())
    print(df['Percent_of_adults_with_a_bachelor_degree_or_higher_2017_21'].mean())

# General function for race-based metrics
def race_metrics(df, race_column):
    print(f"\nMetrics for {race_column}:\n")
    
    # Majority
    df_majority = df[df[race_column] >= 50]
    # print(f"\nCounties with majority {race_column}:\n")
    find_metrics(df)
    
    # # More than 80%
    # df_more_than_80 = df[df[race_column] >= 80]
    # # print(f"\nCounties with more than 80% {race_column}:\n")
    # find_metrics(df_more_than_80)
    
    # # Less than 1%
    # df_less_than_1 = df[df[race_column] <= 1]
    # # print(f"\nCounties with less than 1% {race_column}:\n")
    # find_metrics(df_less_than_1)
    
    # # Max race percentage
    # df_max_race = df[df[race_column] == df['max_race_percentage']]
    # print(f"\nCounties where {race_column} is the max race percentage:\n")
    # find_metrics(df_max_race)
    
    # # Min race percentage
    # df_min_race = df[df[race_column] == df['min_race_percentage']]
    # print(f"\nCounties where {race_column} is the min race percentage:\n")
    # find_metrics(df_min_race)

    # # Top 30 counties with the highest percentage of the race
    # df_top_30 = df.nlargest(30, race_column)
    # print(f"\nTop 30 counties with the highest percentage of {race_column}:\n")
    # find_metrics(df_top_30)

    # # Top 30 counties with the lowest percentage of the race
    # df_bottom_30 = df.nsmallest(30, race_column)
    # print(f"\nTop 30 counties with the lowest percentage of {race_column}:\n")
    # find_metrics(df_bottom_30)

# Adding max and min race percentage columns to df
df['max_race_percentage'] = df[['percentage_white', 'percentage_black_or_african', 'percentage_american_indian_and_native_alaskan', 'percentage_two_or_more_races', 'percentage_hispanic', 'percentage_asian_pacific_american']].max(axis=1)
df['min_race_percentage'] = df[['percentage_white', 'percentage_black_or_african', 'percentage_american_indian_and_native_alaskan', 'percentage_two_or_more_races', 'percentage_hispanic', 'percentage_asian_pacific_american']].min(axis=1)

# List of race columns
# race_columns = [
#     'percentage_white', 
#     'percentage_black_or_african',
#     'percentage_asian_pacific_american',
#     'percentage_american_indian_and_native_alaskan', 
#     'percentage_hispanic', 
#     'percentage_two_or_more_races', 
# ]

race_columns = ['percentage_female']

# Calculate metrics for each race
for race in race_columns:
    race_metrics(df, race)
