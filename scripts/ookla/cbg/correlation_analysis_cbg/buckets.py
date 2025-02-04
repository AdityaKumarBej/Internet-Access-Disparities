import pandas as pd
import matplotlib.pyplot as plt

# Load the data
# file_path = "../../../../results/mlab/US/woodard_research/mlab_woodard_census_providers.csv"  # Replace with your actual file path
file_path = "../../../../results/ookla/US/cbg/raw_masters/state_master_fixed_06_nations.csv"  # Replace with your actual file path
data = pd.read_csv(file_path)

population_density = data['population_density']

# Use qcut to bucket the data into 3 bins with equal distribution
bins, bin_edges = pd.qcut(population_density, q=3, labels=["Low", "Medium", "High"], retbins=True)

# Add the bins as a new column to the dataframe
data['population_density_bin'] = bins

# Output the bin limits
print("Bin limits:", bin_edges)


# pop_density_mean = data['population_density'].mean()
# pop_density_std = data['population_density'].std()
# data_filtered = data[(data['population_density'] >= pop_density_mean - pop_density_std) &
#                      (data['population_density'] <= pop_density_mean + pop_density_std)]

# income_mean = data['median_household_income'].mean()
# income_std = data['median_household_income'].std()
# data_filtered2 = data_filtered[(data_filtered['median_household_income'] >= income_mean - income_std) &
#                      (data_filtered['median_household_income'] <= income_mean + income_std)]

# # Calculate avg and median download speeds for percentage_female < 50
# below_50 = data_filtered2[data_filtered2['percentage_female'] < 50]
# avg_below_50 = below_50['download_avg'].mean()
# median_below_50 = below_50['download_avg'].median()
# print(f"Average download speed when percentage_female < 50: {avg_below_50:.2f} Mbps")
# print(f"Median download speed when percentage_female < 50: {median_below_50:.2f} Mbps")

# # Calculate avg and median download speeds for percentage_female > 50
# above_50 = data_filtered2[data_filtered2['percentage_female'] > 50]
# avg_above_50 = above_50['download_avg'].mean()
# median_above_50 = above_50['download_avg'].median()
# print(f"Average download speed when percentage_female > 50: {avg_above_50:.2f} Mbps")
# print(f"Median download speed when percentage_female > 50: {median_above_50:.2f} Mbps")


