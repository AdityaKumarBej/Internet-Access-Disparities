import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# data = pd.read_csv("../../../results/ookla/US/cbg/masters/ookla_fixed_cbg_master_06_bayarea.csv", low_memory=False)
data = pd.read_csv("../../../../results/ookla/US/cbg/masters/combined_cbg_master.csv", low_memory=False)

# all my columns
relevant_cols = ['total_tests', 'total_devices', 
    'population_density', 'median_household_income',
    'percentage_age_under_5', 'percentage_age_5_17', 'percentage_age_18_64', 'percentage_age_over_65',
    'percentage_male', 'percentage_female',
    'less_than_high_school_diploma', 'high_school_diploma_only', 'bachelor_or_associate_degree', 'masters_or_more',
    'hispanic_latino', 'white_alone', 'black_or_african_american_alone', 'american_indian_and_alaskan_native_alone', 
    'asian_alone', 'native_hawaiian_and_other_pacific_islander_alone', 'two_or_more_races', 'some_other_race_alone'
]

# features selected after random forest feature importance test
selected_columns = [
    'population_density', 'total_devices', 'total_tests', 
    'median_household_income', 'less_than_high_school_diploma', 
    'percentage_age_18_64', 'percentage_age_over_65', 
    'white_alone', 'hispanic_latino',
    'asian_alone', 'black_or_african_american_alone', 'high_school_diploma_only'
]

x = data[selected_columns]
y = data['avg_d_mbps_mean']

x = x.dropna()  # Remove rows with missing values
y = y[x.index]  # Make sure the target matches the features after dropping rows

scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2, random_state=42)

model = GradientBoostingRegressor(random_state=42)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R² Score: {r2}')

feature_importance = model.feature_importances_
for feature, importance in zip(selected_columns, feature_importance):
    print(f'{feature}: {importance}')

# from sklearn.inspection import PartialDependenceDisplay

# # Plot partial dependence using the new method
# display = PartialDependenceDisplay.from_estimator(
#     model, 
#     x_train, 
#     features= selected_columns,
#     feature_names= selected_columns, 
#     grid_resolution=50
# )

# # To show the plot
# import matplotlib.pyplot as plt
# plt.show()