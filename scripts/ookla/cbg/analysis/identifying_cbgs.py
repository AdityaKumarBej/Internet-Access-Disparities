import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def create_density_bins(data, column='population_density', num_bins=3):
    data['Density_Bucket'] = pd.qcut(data[column], q=num_bins, labels=[f'Bin_{i+1}' for i in range(num_bins)], duplicates='drop')
    
    bin_ranges = pd.qcut(data[column], q=num_bins, labels=False, retbins=True)[1]
    
    print('--' * 40)
    print(f'Bay area general info:')
    print('--' * 40)

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
    '''
    ***Needs update for aggregated CBG data***

    Visualize the CBGs on a map with density bins highlighted in different colors.
    '''
    # Convert the DataFrame to a GeoDataFrame
    gdf = gpd.GeoDataFrame(data, geometry=gpd.GeoSeries.from_wkt(data['geometry']))

    # Plot all CBGs
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    gdf.plot(ax=ax, color='lightgrey', markersize=5, label='All CBGs')

    # Highlight Bin_1 CBGs
    bin_1_gdf = gdf[gdf['Density_Bucket'] == 'Bin_1']
    bin_1_gdf.plot(ax=ax, color='lightgreen', markersize=5, label='Bin 1 CBGs')

    # Highlight Bin_2 CBGs
    bin_1_gdf = gdf[gdf['Density_Bucket'] == 'Bin_2']
    bin_1_gdf.plot(ax=ax, color='blue', markersize=5, label='Bin 1 CBGs')

    # Highlight Bin_3 CBGs
    bin_1_gdf = gdf[gdf['Density_Bucket'] == 'Bin_3']
    bin_1_gdf.plot(ax=ax, color='red', markersize=5, label='Bin 1 CBGs')

    plt.title('Bay Area CBGs with Population Density Bins')

    green_patch = mpatches.Patch(color='lightgreen', label='Bin 1 (Green)')
    blue_patch = mpatches.Patch(color='blue', label='Bin 2 (Blue)')
    red_patch = mpatches.Patch(color='red', label='Bin 3 (Red)')

    plt.legend(handles=[green_patch, blue_patch, red_patch], title='Density Bins')
    plt.show()

def cbgs_above_average(data, bin_label='', column_name=''):

    print(f'Total bay area cbgs: {len(data)}')

    bin_data = data[data['Density_Bucket'] == bin_label]

    print(f'Total bay area {bin_label} density cbgs: {len(bin_data)}')

    # bin_avg = bin_data[column_name].mean()
    bin_avg = bin_data[column_name].mean()
    
    higher_cbgs_data = bin_data.loc[bin_data[column_name] > bin_avg, ['GEOID', 'COUNTYFP', 'median_household_income', 'avg_d_mbps_mean', 'avg_d_mbps_median', 'avg_u_mbps_mean', 'avg_u_mbps_median', 'avg_lat_ms_mean', 'avg_lat_ms_median', 'percentage_age_over_65','less_than_high_school_diploma', 'masters_or_more', 'geometry', 'hispanic_latino', 'white_alone', 'black_or_african_american_alone', 'asian_alone']]

    print(f'Total bay area {bin_label} density cbgs with higher than avg {column_name} percentage cbgs: {len(higher_cbgs_data)}')
    print()

    higher_cbgs_list = higher_cbgs_data['GEOID'].unique().tolist()

    # print(f'# unique cbgs from that list:  {len(higher_cbgs_list)}') # we don't care not that we've aggregated the data.

    # print(f'First few: {higher_cbgs_list[:10]}')

    # which counties do these CBGs belong to?
    county_data = data[data['GEOID'].isin(higher_cbgs_list)][['GEOID', 'COUNTYFP', 'median_household_income']].drop_duplicates()

    # county_data = county_data.dropna(subset=['COUNTYFP'])

    county_counts = county_data['COUNTYFP'].value_counts().to_dict()

    print(f'Unique counties from unique cbg list: {len(county_counts)}')

    for county, count in county_counts.items():
        print(f'{county}: {count}')

    '''
    85 : 210 -- Santa Clara
    1  : 164 -- Alameda
    13 : 129 -- Contra Costa

    which means, in santa clara county, there are 210 cbgs who have high asian_alone percentage and also low density
    but still are highly impacted by the asian_alone percentage.
    let's look only at santa clara to try to reason this phenomenon from the income perspective to try to cancel that out:
    '''

    # countyfp = 85
    # countyname = 'Santa Clara' # for now, hardcoding to analyze further

    countyfp = 1
    countyname = 'Alameda' # for now, hardcoding to analyze further

    analyze_county(countyfp, countyname, data, bin_data, higher_cbgs_data, bin_label)

def analyze_county(countyfp, countyname, data, bin_data, higher_cbgs_data, bin_label):
    # the county I'm considering right now

    mycounty = countyname

    print('--' * 40)
    print(f'Now analysing county: {mycounty} (FP: {countyfp})')
    print('--' * 40)
    
    ## all of the cbgs in this county
    mycounty_all_cbgs = data[data['COUNTYFP'] == countyfp]
    print(f'Number of {mycounty} CBGs: {len(mycounty_all_cbgs)}')

    # show_on_map(mycounty_all_cbgs)  # show the map of all CBGs in this county

    mycounty_all_cbgs_filtered = mycounty_all_cbgs[mycounty_all_cbgs['median_household_income'] > 0]
    print(f'CBGs with valid income data: {len(mycounty_all_cbgs_filtered)}')
    # not a lot of difference, so great, very few cbgs have missing income data

    # overall county download speed avg:
    mycounty_overall_speed = mycounty_all_cbgs_filtered['avg_d_mbps_mean'].mean()
    print(f'{mycounty} Overall Download Speed Mean: {mycounty_overall_speed}')

    mycounty_overall_speed_median = mycounty_all_cbgs_filtered['avg_d_mbps_median'].median()
    print(f'{mycounty} Overall Download Speed Median: {mycounty_overall_speed_median}')

    mycounty_overall_column_mean = mycounty_all_cbgs_filtered['hispanic_latino'].mean()
    print(f'Overall {column_name} percentage: {mycounty_overall_column_mean}')

    # overall county income avg:
    mycounty_overall_income = mycounty_all_cbgs_filtered['median_household_income'].mean()
    print(f'{mycounty} Overall Income: {mycounty_overall_income}')

    mycounty_overall_age_over_65 = mycounty_all_cbgs_filtered['percentage_age_over_65'].mean()
    print(f'{mycounty} Overall percentage above 65: {mycounty_overall_age_over_65}')

    mycounty_overall_edu = mycounty_all_cbgs_filtered['less_than_high_school_diploma'].mean()
    print(f'{mycounty} Overall percentage of people less than high school diploma: {mycounty_overall_edu}')

    mycounty_overall_edu_higher = mycounty_all_cbgs_filtered['masters_or_more'].mean()
    print(f'{mycounty} Overall percentage of people with masters or more: {mycounty_overall_edu_higher}')

    # racial demographics
    overall_white = mycounty_all_cbgs_filtered['white_alone'].mean()
    print(f'{mycounty} Overall percentage white_alone: {overall_white}')

    overall_black = mycounty_all_cbgs_filtered['black_or_african_american_alone'].mean()
    print(f'{mycounty} Overall percentage black_or_african_american_alone: {overall_black}')

    overall_asian = mycounty_all_cbgs_filtered['asian_alone'].mean()
    print(f'{mycounty} Overall percentage asian_alone: {overall_asian}')

    print('--' * 25)

    ## {bin_label} density cbgs of this county
    mycounty_bin_density_cbgs = bin_data[bin_data['COUNTYFP'] == countyfp]
    print(f'Number of {mycounty} CBGs in {bin_label}: {len(mycounty_bin_density_cbgs)}')

    # their avg download speed:
    mycounty_bin_density_speed = mycounty_bin_density_cbgs['avg_d_mbps_mean'].mean()
    print(f'{mycounty} Overall Download Speed Mean: {mycounty_bin_density_speed}')

    mycounty_bin_density_speed_median = mycounty_bin_density_cbgs['avg_d_mbps_median'].median()
    print(f'{mycounty} Overall Download Speed Median: {mycounty_bin_density_speed_median}')

    mycounty_bin_column_mean = mycounty_bin_density_cbgs['hispanic_latino'].mean()
    print(f'Overall {column_name} percentage: {mycounty_bin_column_mean}')

    # their avg income:
    mycounty_bin_density_income = mycounty_bin_density_cbgs['median_household_income'][mycounty_bin_density_cbgs['median_household_income'] > 0].mean()
    print(f'{mycounty} {bin_label} Density Income: {mycounty_bin_density_income}')

    mycounty_bin_density_age = mycounty_bin_density_cbgs['percentage_age_over_65'][mycounty_bin_density_cbgs['percentage_age_over_65'] > 0].mean()
    print(f'{mycounty} {bin_label} Density Age: {mycounty_bin_density_age}')

    mycounty_bin_density_edu1 = mycounty_bin_density_cbgs['less_than_high_school_diploma'][mycounty_bin_density_cbgs['less_than_high_school_diploma'] > 0].mean()
    print(f'{mycounty} {bin_label} Density Edu less than HS: {mycounty_bin_density_edu1}')

    mycounty_low_density_edu2 = mycounty_bin_density_cbgs['masters_or_more'][mycounty_bin_density_cbgs['masters_or_more'] > 0].mean()
    print(f'{mycounty} {bin_label} Density Edu more than masters: {mycounty_low_density_edu2}')

    # racial demographics
    density_bin_white = mycounty_bin_density_cbgs['white_alone'].mean()
    print(f'{mycounty} Bin percentage white_alone: {density_bin_white}')

    density_bin_black = mycounty_bin_density_cbgs['black_or_african_american_alone'].mean()
    print(f'{mycounty} Bin percentage black_or_african_american_alone: {density_bin_black}')

    density_bin_asian = mycounty_bin_density_cbgs['asian_alone'].mean()
    print(f'{mycounty} Bin percentage asian_alone: {density_bin_asian}')

    print('--' * 25)

    ## {bin_label} density cbgs of this county with high {column_name}} percentage
    mycounty_high_asian_cbgs = higher_cbgs_data[higher_cbgs_data['COUNTYFP'] == countyfp]
    print(f'Number of {mycounty} CBGs in {bin_label} with high {column_name} WHEN compared with bay area average: {len(mycounty_high_asian_cbgs)}')

    # their avg download speed:
    mycounty_high_asian_speed = mycounty_high_asian_cbgs['avg_d_mbps_mean'].mean()
    print(f'{mycounty} {bin_label} high {column_name} Download Speed Mean: {mycounty_high_asian_speed}')

    mycounty_high_asian_speed_median = mycounty_high_asian_cbgs['avg_d_mbps_median'].median()
    print(f'{mycounty} {bin_label} high {column_name} Download Speed Median: {mycounty_high_asian_speed_median}')

    mycounty_bin_high_mean = mycounty_high_asian_cbgs['hispanic_latino'].mean()
    print(f'Overall {column_name} percentage: {mycounty_bin_high_mean}')

    # their avg income:
    mycounty_high_asian_income = mycounty_high_asian_cbgs['median_household_income'][mycounty_high_asian_cbgs['median_household_income'] > 0].mean()
    print(f'{mycounty} {bin_label} high {column_name} Income: {mycounty_high_asian_income}')

    mycounty_high_asian_age = mycounty_high_asian_cbgs['percentage_age_over_65'][mycounty_high_asian_cbgs['median_household_income'] > 0].mean()
    print(f'{mycounty} {bin_label} high {column_name} percentage age above 65: {mycounty_high_asian_age}')

    mycounty_high_asian_edu1 = mycounty_high_asian_cbgs['less_than_high_school_diploma'][mycounty_high_asian_cbgs['median_household_income'] > 0].mean()
    print(f'{mycounty} {bin_label} high {column_name} percentage of less than highschool diploma: {mycounty_high_asian_edu1}')

    mycounty_high_asian_edu2 = mycounty_high_asian_cbgs['masters_or_more'][mycounty_high_asian_cbgs['median_household_income'] > 0].mean()
    print(f'{mycounty} {bin_label} high {column_name} percentage of more than masters: {mycounty_high_asian_edu2}')

    # racial demographics
    density_bin_white_high_column = mycounty_high_asian_cbgs['white_alone'].mean()
    print(f'{mycounty} High column percentage white_alone: {density_bin_white_high_column}')

    density_bin_black_high_column = mycounty_high_asian_cbgs['black_or_african_american_alone'].mean()
    print(f'{mycounty} High column percentage black_or_african_american_alone: {density_bin_black_high_column}')

    density_bin_asian_high_column = mycounty_high_asian_cbgs['asian_alone'].mean()
    print(f'{mycounty} High column percentage asian_alone: {density_bin_asian_high_column}')

    print('--' * 25)

    print()

    # TO-DO: on the previously created map, among the lightgreen cbgs (low density), update to highlight the ones with high asian_alone percentage
    # highlight_on_map(mycounty_all_cbgs, mycounty_high_asian_cbgs)

    # print("calculating mycounty average...")
    # # but we want low density cbgs of mycounty with high asian_alone percentage IN mycounty not above bay area average
    # mycounty_avg_asian_percentage = mycounty_all_cbgs['asian_alone'].mean()
    # print(f'{mycounty} Average Asian Percentage: {mycounty_avg_asian_percentage}')

    # mycounty_high_asian_cbgs_in_mycounty = mycounty_all_cbgs[mycounty_all_cbgs['asian_alone'] > mycounty_avg_asian_percentage]
    # print(f'Number of {mycounty} CBGs in Bin 1 with high asian_alone WHEN compared with {mycounty} average: {len(mycounty_high_asian_cbgs_in_mycounty)}')

    # # their avg income:
    # mycounty_high_asian_income_in_mycounty = mycounty_high_asian_cbgs_in_mycounty['median_household_income'][mycounty_high_asian_cbgs_in_mycounty['median_household_income'] > 0].mean()
    # print(f'{mycounty} High Asian Income in {mycounty}: {mycounty_high_asian_income_in_mycounty}')

def highlight_on_map(mycounty_all_cbgs, highlight_data):
    """
    Overlay the map with a highlight for specific CBGs (e.g., high asian_alone %).
    Assumes geometry is already in WKT format.
    """
    # Convert the data to a GeoDataFrame
    base_gdf = gpd.GeoDataFrame(mycounty_all_cbgs, geometry=gpd.GeoSeries.from_wkt(mycounty_all_cbgs['geometry']))
    highlighted_gdf = gpd.GeoDataFrame(highlight_data, geometry=gpd.GeoSeries.from_wkt(highlight_data['geometry']))

    # Plot
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    # Plot base CBGs in light grey for context
    base_gdf.plot(ax=ax, color='lightgreen', markersize=5, label='All Highlighted County CBGs (Context)')

    # Plot highlighted CBGs (e.g., Bin 1 + high asian_alone %) in yellow
    highlighted_gdf.plot(ax=ax, color='yellow', markersize=5, label='High Asian in Low-Density')

    plt.title('Highlighted CBGs with High Asian % (Low-Density)')
    yellow_patch = mpatches.Patch(color='yellow', label='High Asian % (Bin 1)')
    plt.legend(handles=[yellow_patch])
    # plt.show()


file_paths = {
    'california': "../../../../../results/ookla/US/cbg/raw_masters/state_master_fixed_06.csv",

    'elnorte': "../../../../../results/ookla/US/cbg/raw_masters/nation_master_fixed_06_EL NORTE.csv",
    'thefarwest': "../../../../../results/ookla/US/cbg/raw_masters/nation_master_fixed_06_THE FAR WEST.csv",
    'theleftcoast': "../../../../../results/ookla/US/cbg/raw_masters/nation_master_fixed_06_THE LEFT COAST.csv",

    'elnorte_ventura': "../../../../../results/ookla/US/cbg/raw_census/ookla_fixed_cbg_06_111_census.csv",
    'thefarwest_fresno': "../../../../../results/ookla/US/cbg/raw_census/ookla_fixed_cbg_06_019_census.csv",
    'theleftcoast_santaclara': "../../../../../results/ookla/US/cbg/raw_census/ookla_fixed_cbg_06_085_census.csv",

    # aggregared
    'bayarea': "../../../../../results/ookla/US/cbg/masters/ookla_fixed_cbg_master_06_bayarea.csv",

    'middlecalifornia': "../../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_06_middlecalifornia.csv",
    'losangelesarea': "../../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_06_losangelesarea.csv",
    'dallasarea': "../../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_48_dallasarea.csv",
    'houstonarea': "../../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_48_houstonarea.csv",
    'southtexasarea': "../../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_48_southtexasarea.csv",
}

file_path = file_paths['bayarea']

data = pd.read_csv(file_path, low_memory=False)

data = create_density_bins(data, column='population_density', num_bins=3)

columns =['hispanic_latino']
# , 'hispanic_latino', 'less_than_high_school_diploma']

for column_name in columns:
    population_density_wise_averages(data, column_name)
    print()

# show_on_map(data)

cbgs_above_average(data, bin_label='Bin_3', column_name='hispanic_latino')

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

