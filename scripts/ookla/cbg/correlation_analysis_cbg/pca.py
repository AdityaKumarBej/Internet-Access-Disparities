import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

input_file = "../../../../results/ookla/US/cbg/raw_masters/state_master_fixed_06_nations.csv"

data = pd.read_csv(input_file)

# 'population_density',

features = [ 'avg_d_mbps', 
    'median_household_income', 'percentage_female',
    'percentage_age_over_65', 
    'less_than_high_school_diploma',
    'hispanic_latino', 'black_or_african_american_alone', 'asian_alone'
]
data = data.dropna(subset=features)

X = data[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=2)
pca_components = pca.fit_transform(X_scaled)

data['PC1'] = pca_components[:, 0]
data['PC2'] = pca_components[:, 1]

state_centroid = data[['PC1', 'PC2']].mean()

nation_centroids = data.groupby('nation_name')[['PC1', 'PC2']].mean()

print("State Centroid:")
print(state_centroid)

print("\nWoodard Nation Centroids:")
print(nation_centroids)

plt.figure(figsize=(10, 6))

scatter = plt.scatter(data['PC1'], data['PC2'], c=data['nation_name'].astype('category').cat.codes, cmap='viridis')

# Title and labels
plt.title("PCA: Counties in California with State & Nation Centroids")
plt.xlabel('PC1')
plt.ylabel('PC2')

# state centroid
plt.scatter(state_centroid[0], state_centroid[1], color='red', label='State Centroid', s=200, marker='X')

# nation centroids
for nation, centroid in nation_centroids.iterrows():
    plt.scatter(centroid['PC1'], centroid['PC2'], label=f'{nation} Centroid', s=200, marker='o')

# Creating a custom legend for the nation names
# Get the unique nation names and map them to their corresponding color
nation_labels = data['nation_name'].unique()
for i, nation in enumerate(nation_labels):
    plt.scatter([], [], c=[scatter.cmap(i / len(nation_labels))], label=nation, marker='o')

plt.legend()
plt.grid(True)
plt.show()


