import pandas as pd

data = pd.read_csv('../../../results/ookla/USA/OOKLA_mobile_Woodard_w_census_2019_2023 copy.csv')

# Remove "County" from the NAMELSAD column
data['NAMELSAD'] = data['NAMELSAD'].str.replace(' County', '')

# Save the modified data to a new CSV file
data.to_csv('../../../results/ookla/USA/OOKLA_mobile_Woodard_w_census_2019_2023_nocounty.csv', index=False)

print("Word 'County' removed from NAMELSAD column and saved to modified_file.csv")
