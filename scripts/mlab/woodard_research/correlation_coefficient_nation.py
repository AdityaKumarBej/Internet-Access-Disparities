import pandas as pd
from scipy.stats import pearsonr
import numpy as np

# Load the data from the CSV file into a DataFrame
df = pd.read_csv('../../../results/mlab/US/Woodard_research/mlab_woodard_w_popcount_hhincome_education_age.csv')

# Filter the DataFrame for the year 2023
df_2023 = df[df['year'] == 2023]

# Drop rows with missing or infinite values in the specified columns
df_cleaned = df_2023.dropna(subset=['median_household_income', 'download_avg'])
df_cleaned = df_cleaned.replace([np.inf, -np.inf], np.nan).dropna(subset=['median_household_income', 'download_avg'])

# Group the DataFrame by state_name
grouped = df_cleaned.groupby('WOODARD NATION NAME')

# Create an empty DataFrame to store the correlation coefficients, average download speed, and average household income
correlation_df = pd.DataFrame(columns=['nation_name', 'income_download_correlation', 'avg_download_speed', 'avg_household_income'])

# Calculate and store the correlation coefficients, average download speed, and average household income for each state
for state_name, group in grouped:
    download_speed = group['download_avg']
    income = group['median_household_income']
    
    # Check if there are at least two data points available
    if len(download_speed) >= 2 and len(income) >= 2:
        income_download_corr, _ = pearsonr(income, download_speed)
    else:
        # If there are not enough data points, set the correlation coefficient to NaN
        income_download_corr = np.nan
    
    # Calculate the average download speed and average household income
    avg_download_speed = download_speed.mean()
    avg_household_income = income.mean()
    
    correlation_df = correlation_df.append({'nation_name': state_name,
                                            'income_download_correlation': income_download_corr,
                                            'avg_download_speed': avg_download_speed,
                                            'avg_household_income': avg_household_income},
                                           ignore_index=True)

# Write the DataFrame to a CSV file
correlation_df.to_csv('../../../results/mlab/US/Woodard_research/correlation_coefficients_by_nation.csv', index=False)
