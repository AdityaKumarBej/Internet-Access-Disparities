import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# File paths for different regions
file_paths = {
    'bayarea': "../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_06_bayarea.csv",
    'middlecalifornia': "../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_06_middlecalifornia.csv",
    'losangelesarea': "../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_06_losangelesarea.csv",
    # Add other regions as needed
}

# Define relevant columns for feature importance
relevant_cols = [ 
    'median_household_income', 'percentage_female',
    'percentage_age_18_64', 'percentage_age_over_65', 
    'less_than_high_school_diploma', 'masters_or_more',
    'hispanic_latino', 'white_alone', 'black_or_african_american_alone', 'asian_alone'
]

# Colors for each region
colors = {
    'bayarea': 'red',
    'middlecalifornia': 'green',
    'losangelesarea': 'yellow',
    # Add other regions with different colors
}

# Initialize a list to hold feature importances for each region
importances = {region: [] for region in file_paths}

# Iterate over file paths and train Random Forest for each region
for region, file_path in file_paths.items():
    # Read the data
    data = pd.read_csv(file_path, low_memory=False)
    data = data.dropna(subset=relevant_cols + ['avg_d_mbps'])

    X = data[relevant_cols]
    y = data['avg_d_mbps']

    # Scale the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Train the Random Forest model
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    # Get feature importance for the current region
    feature_importance = rf.feature_importances_

    # Store the feature importances for the current region
    importances[region] = feature_importance

# Prepare the plot
fig, ax = plt.subplots(figsize=(12, 6))

# Set the bar width
bar_width = 0.1
index = np.arange(len(relevant_cols))

# Plot the feature importance for each region
for i, (region, importance) in enumerate(importances.items()):
    ax.barh(index + i * bar_width, importance, bar_width, color=colors[region], label=region)

# Add labels and title
ax.set_xlabel('Importance')
ax.set_ylabel('Feature')
ax.set_title('Feature Importance by Region')
ax.set_yticks(index + bar_width * (len(file_paths) - 1) / 2)
ax.set_yticklabels(relevant_cols)
ax.legend(title='Region')

plt.gca().invert_yaxis()  # Invert y-axis for better readability
plt.show()
