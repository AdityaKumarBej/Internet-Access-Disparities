import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def create_density_bins(data, column='population_density', num_bins=3):
    data['Density_Bucket'] = pd.qcut(data[column], q=num_bins, labels=[f'Bin_{i+1}' for i in range(num_bins)], duplicates='drop')
    
    bin_ranges = pd.qcut(data[column], q=num_bins, labels=False, retbins=True)[1]
    
    for i in range(1, num_bins+1):
        bin_range = (bin_ranges[i-1], bin_ranges[i])
        bin_count = data[data['Density_Bucket'] == f'Bin_{i}'].shape[0]
        print(f'Bin {i}: Count: {bin_count} : {bin_range[0]} to {bin_range[1]}')
    print()
    return data

def population_density_wise_averages(data, column_name):
    average_column = data[column_name].mean()

    print(f'overall {column_name} column average: {average_column}')
    
    for i in range(1, 4):
        density_data = data[data['Density_Bucket'] == f'Bin_{i}']
        average_column_density = density_data[column_name].mean()
        
        print(f'Bin {i} cbgs, {column_name} column average is : {average_column_density}')

    # geoids = low_density_data.loc[low_density_data['asian_alone'] > average_column, 'GEOID'].unique()

    # print(geoids.tolist())
    # print(len(geoids))

def show_on_map(data):
    # Convert the DataFrame to a GeoDataFrame
    gdf = gpd.GeoDataFrame(data, geometry=gpd.GeoSeries.from_wkt(data['ookla_geometry']))

    # Plot all CBGs
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    gdf.plot(ax=ax, color='lightgrey', markersize=5, label='All CBGs')

    # Highlight Bin_1 CBGs
    bin_1_gdf = gdf[gdf['Density_Bucket'] == 'Bin_1']
    bin_1_gdf.plot(ax=ax, color='green', markersize=5, label='Bin 1 CBGs')

    # Highlight Bin_2 CBGs
    bin_1_gdf = gdf[gdf['Density_Bucket'] == 'Bin_2']
    bin_1_gdf.plot(ax=ax, color='blue', markersize=5, label='Bin 1 CBGs')

    # Highlight Bin_3 CBGs
    bin_1_gdf = gdf[gdf['Density_Bucket'] == 'Bin_3']
    bin_1_gdf.plot(ax=ax, color='red', markersize=5, label='Bin 1 CBGs')

    plt.title('Bay Area CBGs with Population Density Bins')

    green_patch = mpatches.Patch(color='green', label='Bin 1 (Green)')
    blue_patch = mpatches.Patch(color='blue', label='Bin 2 (Blue)')
    red_patch = mpatches.Patch(color='red', label='Bin 3 (Red)')

    plt.legend(handles=[green_patch, blue_patch, red_patch], title='Density Bins')
    plt.show()

def cbgs_above_average(data, bin_label='Bin_1', column_name='asian_alone'):

    print(len(data))

    bin_data = data[data['Density_Bucket'] == bin_label]

    print(len(bin_data))

    bin_avg = bin_data[column_name].mean()
    
    higher_cbgs_data = bin_data.loc[bin_data[column_name] > bin_avg, ['GEOID', 'COUNTYFP', 'median_household_income']]

    print(len(higher_cbgs_data))
    
    higher_cbgs_list = higher_cbgs_data['GEOID'].unique().tolist()

    print(len(higher_cbgs_list))

    print(f'Number of CBGs with higher {column_name}: {len(higher_cbgs_list)}')
    print(f'First few: {higher_cbgs_list[:10]}')

    # which counties do these CBGs belong to?
    county_data = data[data['GEOID'].isin(higher_cbgs_list)][['GEOID', 'COUNTYFP', 'median_household_income']].drop_duplicates()

    county_data = county_data.dropna(subset=['COUNTYFP'])

    print(len(county_data))

    county_counts = county_data['COUNTYFP'].value_counts().to_dict()

    print(f'County FP: Number of CBGs in the county with higher {column_name} in {bin_label}')
    for county, count in county_counts.items():
        print(f'{county}: {count}')

    # Aalameda (1)      : 65
    # Martinez (13)     : 57
    # Santa Clara (85)  : 56

    # which means, in alameda county, there are 65 cbgs who have high asian_alone percentage and also low density
    # but still are highly impacted by the asian_alone percentage.
    # let's look only at alameda to try to reason this phenomenon from the income perspective to try to cancel that out:

    # Filter out negative values before calculating the mean
    # all of alameda cbgs
    alameda_overall_income = data[data['COUNTYFP'] == 1]['median_household_income'][data['median_household_income'] > 0].mean()

    print(alameda_overall_income)

    # low density cbgs of alameda
    alameda_overall_income = bin_data[bin_data['COUNTYFP'] == 1]['median_household_income'][bin_data['median_household_income'] > 0].mean()

    print(alameda_overall_income)

    # low density cbgs of alameda with high asian_alone percentage
    alameda_filtered_income = county_data[county_data['COUNTYFP'] == 1]['median_household_income'][county_data['median_household_income'] > 0].mean()

    print(alameda_filtered_income)

    # updated code:
    # all of alameda cbgs
    alameda_all_cbgs = data[data['COUNTYFP'] == 1]
    print(f'Number of Alameda CBGs: {len(alameda_all_cbgs)}')

    alameda_all_cbgs_filtered = alameda_all_cbgs[alameda_all_cbgs['median_household_income'] > 0]
    print(f'Number of Alameda CBGs with valid income data: {len(alameda_all_cbgs_filtered)}')
    # not a lot of difference, so great, very few cbgs have missing income data

    # alamdea overall income:
    alameda_overall_income = alameda_all_cbgs_filtered['median_household_income'].mean()
    print(f'Alameda Overall Income: {alameda_overall_income}')

    # low density cbgs of alameda
    alameda_low_density_cbgs = bin_data[bin_data['COUNTYFP'] == 1]
    print(f'Number of Alameda CBGs in Bin 1: {len(alameda_low_density_cbgs)}')
    # their avg income:
    alameda_low_density_income = alameda_low_density_cbgs['median_household_income'][alameda_low_density_cbgs['median_household_income'] > 0].mean()
    print(f'Alameda Low Density Income: {alameda_low_density_income}')

    # low density cbgs of alameda with high asian_alone percentage
    alameda_high_asian_cbgs = higher_cbgs_data[higher_cbgs_data['COUNTYFP'] == 1]
    print(f'Number of Alameda CBGs in Bin 1 with high asian_alone WHEN compared with bay area average: {len(alameda_high_asian_cbgs)}')
    # their avg income:
    alameda_high_asian_income = alameda_high_asian_cbgs['median_household_income'][alameda_high_asian_cbgs['median_household_income'] > 0].mean()
    print(f'Alameda High Asian Income: {alameda_high_asian_income}')

    print()
    print("calculating alameda average...")
    # but we want low density cbgs of alameda with high asian_alone percentage IN ALAMEDA not above bay area average
    alameda_avg_asian_percentage = alameda_all_cbgs['asian_alone'].mean()
    print(f'Alameda Average Asian Percentage: {alameda_avg_asian_percentage}')

    alameda_high_asian_cbgs_in_alameda = alameda_all_cbgs[alameda_all_cbgs['asian_alone'] > alameda_avg_asian_percentage]
    print(f'Number of Alameda CBGs in Bin 1 with high asian_alone WHEN compared with Alameda average: {len(alameda_high_asian_cbgs_in_alameda)}')

    # their avg income:
    alameda_high_asian_income_in_alameda = alameda_high_asian_cbgs_in_alameda['median_household_income'][alameda_high_asian_cbgs_in_alameda['median_household_income'] > 0].mean()
    print(f'Alameda High Asian Income in Alameda: {alameda_high_asian_income_in_alameda}')

file_paths = {
    'california': "../../../../../results/ookla/US/cbg/raw_masters/state_master_fixed_06.csv",

    'elnorte': "../../../../../results/ookla/US/cbg/raw_masters/nation_master_fixed_06_EL NORTE.csv",
    'thefarwest': "../../../../../results/ookla/US/cbg/raw_masters/nation_master_fixed_06_THE FAR WEST.csv",
    'theleftcoast': "../../../../../results/ookla/US/cbg/raw_masters/nation_master_fixed_06_THE LEFT COAST.csv",

    'elnorte_ventura': "../../../../../results/ookla/US/cbg/raw_census/ookla_fixed_cbg_06_111_census.csv",
    'thefarwest_fresno': "../../../../../results/ookla/US/cbg/raw_census/ookla_fixed_cbg_06_019_census.csv",
    'theleftcoast_santaclara': "../../../../../results/ookla/US/cbg/raw_census/ookla_fixed_cbg_06_085_census.csv",


    'bayarea': "../../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_06_bayarea.csv",
    'middlecalifornia': "../../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_06_middlecalifornia.csv",
    'losangelesarea': "../../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_06_losangelesarea.csv",
    'dallasarea': "../../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_48_dallasarea.csv",
    'houstonarea': "../../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_48_houstonarea.csv",
    'southtexasarea': "../../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_48_southtexasarea.csv",
}

file_path = file_paths['bayarea']

data = pd.read_csv(file_path, low_memory=False)

data = create_density_bins(data, column='population_density', num_bins=3)

columns =['asian_alone']
# , 'hispanic_latino', 'less_than_high_school_diploma']

for column_name in columns:
    population_density_wise_averages(data, column_name)
    print()

show_on_map(data)

cbgs_above_average(data, bin_label='Bin_1', column_name='asian_alone')

# ------ thought process ------

# so let me just look at the low pop density cbgs, even if they have low asian_alone percentage
# I want to map them out. where are they?
# my data for this right now has multiple rows for each cbg.. what to do? let's see - how does this still print?

# low_density_data = data[data['Density_Bucket'] == 'Bin_1']
# print(low_density_data.shape)
# print(low_density_data['asian_alone'].mean())
# print(low_density_data['asian_alone'].std())
# print(low_density_data['asian_alone'].max())
# print(low_density_data['asian_alone'].min())
# print(low_density_data['asian_alone'].median())

