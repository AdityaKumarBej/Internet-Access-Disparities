import pandas as pd

# Read the CSV file
df = pd.read_csv("../../../results/mlab/US/Woodard_research/mlab_woodard_w_popcount_hhincome_education_age.csv")

# Count of rows changed
rows_changed = 0

# Loop through each row
for index, row in df.iterrows():
    # Check the length of geoid
    if len(str(row['geoid'])) < 4:
        # Add leading zeroes to make length 4
        df.at[index, 'geoid'] = str(row['geoid']).zfill(4)
        rows_changed += 1

# Write the updated DataFrame back to CSV
df.to_csv("your_updated_file.csv", index=False)

print("Number of rows changed:", rows_changed)
