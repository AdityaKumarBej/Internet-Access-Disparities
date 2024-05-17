import pandas as pd

# # Read the two CSV files
# df1 = pd.read_csv("../../../results/mlab/US/Yearly Masters/combined_data.csv")
# df2 = pd.read_csv("../../../results/mlab/US/Woodard_research/mlab_woodard_w_popcount_hhincome_education_age.csv")

# # Find the difference between the two DataFrames
# extra_rows = df2[~df2.isin(df1)].dropna()

# # Write the difference to a new CSV file
# extra_rows.to_csv("result.csv", index=False)

# # Print the number of extra rows
# print("Number of extra rows in two.csv:", len(extra_rows))


# # Read the CSV file
# df = pd.read_csv("../../../results/mlab/US/Woodard_research/mlab_woodard.csv")

# # Drop all duplicate rows
# df_no_duplicates = df.drop_duplicates()

# # Save the DataFrame without duplicates to a new CSV file
# df_no_duplicates.to_csv("../../../results/mlab/US/Woodard_research/mlab_woodard_no_duplicates.csv", index=False)


# Read the CSV file
df = pd.read_csv("../../../results/ookla/USA/ookla_fixed_woodard_w_popcount_hhincome_education_age.csv")

# Find duplicate rows based on specified columns
duplicate_rows = df[df.duplicated(subset=['geoid','Year'], keep=False)]

duplicate_rows.to_csv('result.csv')

