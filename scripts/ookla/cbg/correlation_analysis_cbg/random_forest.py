import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import time


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

file_path = file_paths['losangelesarea']

data = pd.read_csv(file_path, low_memory=False)

# 'population_density', 'tests', 'devices'
relevant_cols = [
    'median_household_income', 'percentage_female',
    'percentage_age_over_65', 
    'less_than_high_school_diploma',
    'hispanic_latino', 'black_or_african_american_alone', 'asian_alone'
]

start_time = time.time()

data = data.dropna(subset=relevant_cols + ['avg_d_mbps'])

X = data[relevant_cols]
y = data['avg_d_mbps']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# X_scaled = X

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.4, random_state=42)

# rf = RandomForestRegressor(n_estimators=100, random_state=42)

# print(len(X_train))

rf = RandomForestRegressor(n_estimators=200, max_depth=20, min_samples_split=5, random_state=42)

rf.fit(X_train, y_train)

feature_importance = rf.feature_importances_
importance_df = pd.DataFrame({'Feature': relevant_cols, 'Importance': feature_importance})

# Correlation with target - for direction
correlation = X.corrwith(y)
correlation_df = pd.DataFrame({'Feature': relevant_cols, 'Correlation': correlation})

result_table = pd.merge(importance_df, correlation_df, on='Feature').sort_values(by='Importance', ascending=False)

print(f"Feature Importance and Correlation for {file_path}:")
print(result_table)
# result_table.to_csv('result_table.csv', sep=';', index=False)

y_pred = rf.predict(X_test)
print("R² Score;", r2_score(y_test, y_pred))
print("MAE;", mean_absolute_error(y_test, y_pred))
print("RMSE;", np.sqrt(mean_squared_error(y_test, y_pred)))

end_time = time.time()  # End the timer
elapsed_time = end_time - start_time
print(f"Time (s); {elapsed_time:.2f}")

# ----------------------------------------------
# eg. percentage_age_over_65 = 0.094864, on average (among 10 runs), removing the percentage_age_over_65 feature decreases the model's performance by about 9.4%

from sklearn.inspection import permutation_importance

result = permutation_importance(rf, X_test, y_test, n_repeats=10, random_state=42)
# print(result.importances_mean)

importance_df = pd.DataFrame({
    'Feature': relevant_cols,
    'Importance': result.importances_mean
})
importance_df_sorted = importance_df.sort_values(by='Importance', ascending=False)

print(importance_df_sorted)

# ----------------------------------------------
# Null model importance
# If the target value is randomly shuffled, do the featues still determine the predicted speeds?
# A negative value everywhere says "no". Which is good. 
# The null model's negative values indicate that when the target is random, the features do not contribute to predictions meaningfully, which is expected.
# The null model importances being negative reinforces the idea that the features are informative, not random noise, and that the random shuffling of the target doesn't lead to significant contributions.

import numpy as np
import random

y_test_array = np.array(y_test)
np.random.shuffle(y_test_array)
result_null = permutation_importance(rf, X_test, y_test_array, n_repeats=10, random_state=42)

print(f"Null Model Importances: {result_null.importances_mean}")

# ----------------------------------------------
# # partial dependence calculation
# # USE X AXIS before scaling for correct labelling

# from sklearn.inspection import plot_partial_dependence

# fig, ax = plt.subplots(figsize=(10, 6))
# plot_partial_dependence(rf, X_train, features=range(len(relevant_cols)), feature_names=relevant_cols, ax=ax)
# plt.xlabel('Feature Values (Original Scale)')
# plt.ylabel('Predicted avg_d_mbps')
# plt.show()

# ----------------------------------------------
# # Check For Overfitting - Perform cross-validation (e.g., 5-fold)
# # results show that our model is doing very bad. worse than just predicting the average.

# from sklearn.model_selection import cross_val_score

# cv_scores = cross_val_score(rf, X, y, cv=5, scoring='r2')  # 'r2' for R² score
# print(f"Mean R² across folds: {cv_scores.mean()}")

# ----------------------------------------------
# # calculate correlation between the attributes

# import seaborn as sns

# correlation_matrix = X.corr()
# plt.figure(figsize=(10, 8))
# sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", cbar=True)
# plt.title('Correlation Matrix')
# plt.show()

# ----------------------------------------------
# # SHAP visualizes the contribution of each feature to the model’s predictions
# not really useful for my analysis

# import shap

# # Use your model and dataset
# X = data[[
#     'median_household_income', 'percentage_female',
#     'percentage_age_over_65', 
#     'less_than_high_school_diploma',
#     'hispanic_latino', 'black_or_african_american_alone', 'asian_alone'
# ]]
# y = data["avg_d_mbps"]

# # Explainer for Random Forest
# explainer = shap.Explainer(rf, X)
# shap_values = explainer(X)

# # SHAP Summary Plot
# shap.summary_plot(shap_values, X)

# ----------------------------------------------
# plot graphs
# red bar if negative correlation
# colors = result_table['Correlation'].apply(lambda x: 'red' if x < 0 else 'skyblue')

# plt.figure(figsize=(10, 6))
# plt.barh(result_table['Feature'], result_table['Importance'], color=colors)
# plt.xlabel('Importance')
# plt.ylabel('Feature')
# plt.title('Feature Importance')
# plt.gca().invert_yaxis()  # To display the most important features at the top
# plt.show()

# ----------------------------------------------
# # # calculate VIF - Multicollinearity check
# from statsmodels.stats.outliers_influence import variance_inflation_factor
# from statsmodels.tools.tools import add_constant

# X_with_const = add_constant(X_scaled)  # Add constant for intercept calculation
# vif_data = pd.DataFrame()
# vif_data['Feature'] = ['const'] + relevant_cols
# vif_data['VIF'] = [variance_inflation_factor(X_with_const, i) for i in range(X_with_const.shape[1])]

# print(vif_data)

# ---------------------------------------------------
# # tuning hyperparameters for best model performance
# from sklearn.model_selection import GridSearchCV
# from sklearn.model_selection import RandomizedSearchCV
# Best Parameters: {'max_depth': 20, 'min_samples_split': 5, 'n_estimators': 200}
# param_dist = {
#     'n_estimators': [50, 100, 200],
#     'max_depth': [None, 10, 20],
#     'min_samples_split': [2, 5],
# }
# random_search = RandomizedSearchCV(RandomForestRegressor(random_state=42), param_dist, n_iter=10, cv=3)
# random_search.fit(X_train, y_train)
# print("Best Parameters:", random_search.best_params_)
