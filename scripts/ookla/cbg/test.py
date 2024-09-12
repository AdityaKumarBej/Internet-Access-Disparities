import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Load the CSV file
df = pd.read_csv('../../../results/ookla/US/cbg/masters/ookla_fixed_cbg_master_06_bayarea.csv') 

# Define your groups
speeds = ['avg_d_mbps_mean', 'avg_d_mbps_median']  # Replace with your actual speed columns
attributes = ['population_density', 'median_household_income', 'percentage_male', 'percentage_age_over_65']   # Replace with your actual attribute columns

df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(subset=speeds + attributes, inplace=True)

# Create an empty DataFrame for p-values
p_values = pd.DataFrame(np.ones((len(speeds), len(attributes))), 
                        columns=attributes, 
                        index=speeds)

# Create an empty DataFrame for correlation coefficients
correlation_matrix = pd.DataFrame(np.zeros((len(speeds), len(attributes))), 
                                  columns=attributes, 
                                  index=speeds)

# Calculate correlation coefficients and p-values
for speed_col in speeds:
    for attr_col in attributes:
        corr, p_val = pearsonr(df[speed_col], df[attr_col])
        correlation_matrix.loc[speed_col, attr_col] = corr
        p_values.loc[speed_col, attr_col] = p_val

# Plot the heatmap for correlation coefficients
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Coefficient Heatmap (Speeds vs Attributes)')
plt.show()

# Plot the heatmap for p-values
plt.figure(figsize=(10, 8))
sns.heatmap(p_values, annot=True, cmap='coolwarm', vmin=0, vmax=0.05)
plt.title('P-value Heatmap (Speeds vs Attributes)')
plt.show()