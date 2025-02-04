import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

file_paths = {
    'california': "../../../../results/ookla/US/cbg/raw_masters/state_master_fixed_06.csv",

    'elnorte': "../../../../results/ookla/US/cbg/raw_masters/nation_master_fixed_06_EL NORTE.csv",
    'thefarwest': "../../../../results/ookla/US/cbg/raw_masters/nation_master_fixed_06_THE FAR WEST.csv",
    'theleftcoast': "../../../../results/ookla/US/cbg/raw_masters/nation_master_fixed_06_THE LEFT COAST.csv",

    'elnorte_ventura': "../../../../results/ookla/US/cbg/raw_census/ookla_fixed_cbg_06_111_census.csv",
    'thefarwest_fresno': "../../../../results/ookla/US/cbg/raw_census/ookla_fixed_cbg_06_019_census.csv",
    'theleftcoast_santaclara': "../../../../results/ookla/US/cbg/raw_census/ookla_fixed_cbg_06_085_census.csv",


    'bayarea': "../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_06_bayarea.csv",
    'middlecalifornia': "../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_06_middlecalifornia.csv",
    'losangelesarea': "../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_06_losangelesarea.csv",
    'dallasarea': "../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_48_dallasarea.csv",
    'houstonarea': "../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_48_houstonarea.csv",
    'southtexasarea': "../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_48_southtexasarea.csv",
}

file_path = file_paths['bayarea']
data = pd.read_csv(file_path, low_memory=False)

# features selected after random forest
selected_columns = [
    'median_household_income', 'percentage_female',
    'percentage_age_over_65', 'less_than_high_school_diploma',
    'hispanic_latino', 'black_or_african_american_alone', 'asian_alone'
]

# drop NaN values in both X and y
df = data[selected_columns + ['avg_d_mbps']].dropna().reset_index(drop=True)

X = df[selected_columns]
y = df['avg_d_mbps']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = GradientBoostingRegressor(
    n_estimators=300,
    learning_rate=0.01, # original 0.05
    max_depth=3, # original 4
    subsample=0.8,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# model stats
print(f'Mean Squared Error: {mse:.2f}')
print(f'R² Score: {r2:.4f}')

# model results - Feature Importance
feature_importance = model.feature_importances_
sorted_features = sorted(zip(selected_columns, feature_importance), key=lambda x: x[1], reverse=True)

print("\nFeature Importances:")
for feature, importance in sorted_features:
    print(f'{feature}: {importance:.4f}')

# additional step 1: Cross-validation for more robust performance estimation
cv_r2_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
print(f'Mean R² across folds: {np.mean(cv_r2_scores):.4f}')

from sklearn.inspection import PartialDependenceDisplay

# Plot partial dependence using the new method
display = PartialDependenceDisplay.from_estimator(
    model, 
    X_train, 
    features= selected_columns,
    feature_names= selected_columns, 
    grid_resolution=50
)

# To show the plot
import matplotlib.pyplot as plt
plt.show()