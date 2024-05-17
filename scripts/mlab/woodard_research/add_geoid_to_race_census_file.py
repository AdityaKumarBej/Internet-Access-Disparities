import pandas as pd

# Load the CSV file
csv_file_path = '../../../datasets/CENSUS/US/Race.csv'
df = pd.read_csv(csv_file_path)

# Ensure STATE and COUNTY are treated as strings, then create 'geoid' by combining them
df['STATE'] = df['STATE'].astype(str).str.zfill(2)  # Ensure STATE is two digits
df['COUNTY'] = df['COUNTY'].astype(str).str.zfill(3)  # Ensure COUNTY is three digits
df['geoid'] = df['STATE'] + df['COUNTY']

# year 2021 = 3 and all ages = 0
df_filtered = df[(df['YEAR'] == 3) & (df['AGEGRP'] == 0)]

# Drop the temporary STATE and COUNTY columns if you do not need them
# df.drop(['STATE', 'COUNTY'], axis=1, inplace=True)

# Save the modified DataFrame to a new CSV file
output_csv_path = '../../../datasets/CENSUS/US/Race_geoid.csv'
df_filtered.to_csv(output_csv_path, index=False)

print(f'Modified data saved to {output_csv_path}')
