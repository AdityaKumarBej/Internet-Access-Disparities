import pandas as pd

excel_file = '/Users/beja/Desktop/personal/Internet Access Disparities/Internet-Access-Disparities/datasets/CENSUS/US/Education.xlsx'
df_excel = pd.read_excel(excel_file)
csv_file = '/Users/beja/Desktop/personal/Internet Access Disparities/Internet-Access-Disparities/results/ookla/USA/OOKLA_fixed_Woodard_w_census_2019_2023.csv'
df_csv = pd.read_csv(csv_file)

# Prepare the Excel data: convert 'FIPS' to string and remove trailing zeroes
df_excel['FIPS'] = df_excel['FIPS'].astype(str).str.rstrip('.0')

# Prepare the CSV data: convert 'geoid' to string and remove trailing zeroes (if necessary)
df_csv['GEOID'] = df_csv['GEOID'].astype(str).str.rstrip('.0')

# Perform an outer join to find non-matching entries
df_outer = pd.merge(df_csv[['GEOID']], df_excel[['FIPS']], left_on='GEOID', right_on='FIPS', how='outer', indicator=True)

# Filter out rows that didn't match from either side
non_matches = df_outer[df_outer['_merge'] != 'both']

# Print geoids and FIPS that do not have matches
print("Non-matching geoids from CSV:")
print(non_matches[non_matches['_merge'] == 'left_only']['GEOID'].dropna().unique())

print("Non-matching FIPS from Excel:")
print(non_matches[non_matches['_merge'] == 'right_only']['FIPS'].dropna().unique())
