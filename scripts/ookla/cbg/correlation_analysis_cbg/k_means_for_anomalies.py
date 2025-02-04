import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

state_fips = '06'
input_file =f"../../../../results/ookla/US/cbg/census/ookla_fixed_cbg_{state_fips}_075_census.csv"
output_file =f"../../../../results/ookla/US/cbg/census/ookla_fixed_cbg_{state_fips}_075_census_k.csv"

df = pd.read_csv(input_file)

# Remove rows with missing values
df = df.dropna(subset=['population_density', 'median_household_income'])

# Normalization
scaler = MinMaxScaler()
df[['norm_population_density', 'norm_median_household_income']] = scaler.fit_transform(df[['population_density', 'median_household_income']])

# K-means Clustering
num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(df[['norm_population_density', 'norm_median_household_income']])

# Function to identify outliers based on IQR
def identify_outliers(data):
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return (data < lower_bound) | (data > upper_bound)

# Create a column to mark outliers
df['is_outlier'] = False

# Apply outlier detection for each cluster
for cluster in df['cluster'].unique():
    cluster_data = df[df['cluster'] == cluster]
    outliers = identify_outliers(cluster_data['avg_d_mbps_avg'])
    df.loc[df['cluster'] == cluster, 'is_outlier'] = outliers

df.to_csv(output_file, index=False)
print(f'File saved in {output_file}')