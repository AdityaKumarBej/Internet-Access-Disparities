import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# data = pd.read_csv("../../../results/ookla/US/cbg/masters/ookla_fixed_cbg_master_06_bayarea.csv", low_memory=False)
data = pd.read_csv("../../../../results/ookla/US/cbg/masters/combined_cbg_master.csv", low_memory=False)


relevant_cols = ['total_tests', 'total_devices', 
    'population_density', 'median_household_income',
    'percentage_age_under_5', 'percentage_age_5_17', 'percentage_age_18_64', 'percentage_age_over_65',
    'percentage_male', 'percentage_female',
    'less_than_high_school_diploma', 'high_school_diploma_only', 'bachelor_or_associate_degree', 'masters_or_more',
    'hispanic_latino', 'white_alone', 'black_or_african_american_alone', 'american_indian_and_alaskan_native_alone', 
    'asian_alone', 'native_hawaiian_and_other_pacific_islander_alone', 'two_or_more_races', 'some_other_race_alone'
]

data = data.dropna(subset=relevant_cols + ['avg_d_mbps_mean'])

X = data[relevant_cols]
y = data['avg_d_mbps_mean']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

feature_importance = rf.feature_importances_
importance_df = pd.DataFrame({'Feature': relevant_cols, 'Importance': feature_importance}).sort_values(by='Importance', ascending=False)

print("Feature Importance:")
print(importance_df)

# # Plot feature importance
# plt.figure(figsize=(12, 8))
# plt.barh(importance_df['Feature'], importance_df['Importance'], color='skyblue')
# plt.xlabel('Importance Score')
# plt.ylabel('Feature')
# plt.title('Random Forest Feature Importance')
# plt.gca().invert_yaxis()  # Flip for better readability
# plt.tight_layout()
# plt.show()
