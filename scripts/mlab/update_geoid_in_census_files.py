# Adding necessary GEOID to census data before we merge census with mlab data

import pandas as pd

# Load the CSV file
# csv_file_path = '../../../datasets/CENSUS/US/Age.csv'
csv_file_path = '../../../datasets/CENSUS/US/Race.csv'
df = pd.read_csv(csv_file_path)

# Ensure STATE and COUNTY are treated as strings, then create 'geoid' by combining them
df['STATE'] = df['STATE'].astype(str).str.zfill(2)  # Ensure STATE is two digits
df['COUNTY'] = df['COUNTY'].astype(str).str.zfill(3)  # Ensure COUNTY is three digits
df['geoid'] = df['STATE'] + df['COUNTY']

# year 2021 = 3 and all ages = 0
df_filtered = df[(df['YEAR'] == 3) & (df['AGEGRP'] == 0)]

# Save the modified DataFrame to a new CSV file
# output_csv_path = '../../../datasets/CENSUS/US/Age_geoid.csv'
output_csv_path = '../../../datasets/CENSUS/US/Race_geoid.csv'
df_filtered.to_csv(output_csv_path, index=False)

print(f'Modified data saved to {output_csv_path}')
