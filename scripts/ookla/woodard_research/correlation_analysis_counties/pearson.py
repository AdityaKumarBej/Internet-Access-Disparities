import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

df = pd.read_csv('../../../../results/ookla/US/cbg/masters/ookla_fixed_cbg_master_06_middlecaliforniaarea.csv') 

speeds = ['avg_d_mbps_mean', 'avg_d_mbps_median', 'avg_u_mbps_mean', 'avg_u_mbps_median', 'avg_lat_ms_mean', 'avg_lat_ms_median']
attributes = ['total_tests', 'total_devices', 'population_density', 'median_household_income', 'percentage_male', 'percentage_female', 'percentage_age_under_5', 'percentage_age_5_17', 'percentage_age_18_64', 'percentage_age_over_65', 'less_than_high_school_diploma', 'high_school_diploma_only', 'bachelor_or_associate_degree' ,'masters_or_more', 'hispanic_latino', 'white_alone', 'black_or_african_american_alone', 'american_indian_and_alaskan_native_alone', 'asian_alone', 'native_hawaiian_and_other_pacific_islander_alone', 'two_or_more_races', 'some_other_race_alone']   # Replace with your actual attribute columns

df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(subset=speeds + attributes, inplace=True)

p_values = pd.DataFrame(np.ones((len(speeds), len(attributes))), 
                        columns=attributes, 
                        index=speeds)

correlation_matrix = pd.DataFrame(np.zeros((len(speeds), len(attributes))), 
                                  columns=attributes, 
                                  index=speeds)

for speed_col in speeds:
    for attr_col in attributes:
        corr, p_val = pearsonr(df[speed_col], df[attr_col])
        correlation_matrix.loc[speed_col, attr_col] = corr
        p_values.loc[speed_col, attr_col] = p_val

correlation_matrix.to_csv("correlation_matrix.csv")
p_values.to_csv("p_values.csv")

# # Plot the heatmap for correlation coefficients
# plt.figure(figsize=(10, 8))
# sns.heatmap(correlation_matrix.rename(index=speeds_new, columns=attributes_new), annot=True, cmap='coolwarm', vmin=-1, vmax=1, annot_kws={"rotation": 90})
# plt.title('Correlation Coefficient Heatmap (Speeds vs Attributes)')
# plt.show()

# # Plot the heatmap for p-values
# plt.figure(figsize=(10, 8))
# sns.heatmap(p_values.rename(index=speeds_new, columns=attributes_new), annot=True, cmap='coolwarm', vmin=0, vmax=0.05, annot_kws={"rotation": 90})
# plt.title('P-value Heatmap (Speeds vs Attributes)')
# plt.show()

# Create a figure with 2 rows and 1 column for vertical (up and down) heatmaps
speeds_new = {
    'avg_d_mbps_mean': 'Mean Speed',
    'avg_d_mbps_median': 'Median Speed', 
}

attributes_new = {
    'population_density': 'Population Density',
    'median_household_income': 'Income',

    'percentage_male': 'Percentage Male',
    'percentage_female': 'Percentage Female',

    'percentage_age_under_5': 'Age < 5',
    'percentage_age_5_17': '5 < Age < 17',
    'percentage_age_18_64': '18 < Age < 64',
    'percentage_age_over_65': 'Age > 65',

    'less_than_high_school_diploma': '< High School',
    'high_school_diploma_only': 'High School Only',
    'bachelor_or_associate_degree': 'Bachelor',
    'masters_or_more': 'Masters or More',

    'hispanic_latino': 'Hispanic',
    'white_alone': 'White',
    'black_or_african_american_alone': 'Black or African American',
    'american_indian_and_alaskan_native_alone': 'American Indian and Alaskan Native',
    'asian_alone': 'Asian',
    'native_hawaiian_and_other_pacific_islander_alone': 'Native Hawaiian',
    'some_other_race_alone': 'Other Race',
    'two_or_more_races': 'Two or More Races'
}



fig, axes = plt.subplots(2, 1, figsize=(10, 12))

# Plot the heatmap for correlation coefficients on the first subplot (top)
sns.heatmap(correlation_matrix.rename(index=speeds_new, columns=attributes_new), 
            annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=axes[0], annot_kws={"rotation": 90})
axes[0].set_title('Correlation Coefficient Heatmap (Speeds vs Attributes)')

# Plot the heatmap for p-values on the second subplot (bottom)
sns.heatmap(p_values.rename(index=speeds_new, columns=attributes_new), 
            annot=False, cmap='coolwarm', vmin=0, vmax=0.1, ax=axes[1], annot_kws={"rotation": 90})
axes[1].set_title('P-value Heatmap')
axes[1].set_xticklabels([])
# Adjust layout to prevent overlap
plt.tight_layout()

# Show both heatmaps
plt.show()

import statsmodels.api as sm

# Prepare the data
X = df[attributes]
y = df[speeds[1]]  # You can loop through or use other speed columns as needed
X = sm.add_constant(X)  # Adds a constant term to the predictor

# Fit the model
model = sm.OLS(y, X).fit()

# Print the summary
print(model.summary())