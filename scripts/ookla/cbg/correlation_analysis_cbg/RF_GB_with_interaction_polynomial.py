# import pandas as pd
# import numpy as np
# from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler, PolynomialFeatures
# from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
# import time

# File path dictionary for different datasets
file_paths = {
    'elnorte_ventura': "../../../../results/ookla/US/cbg/raw_census/ookla_fixed_cbg_06_111_census.csv"
}

# Read the data
file_path = file_paths['elnorte_ventura']
data = pd.read_csv(file_path, low_memory=False)

# # Select relevant columns
# relevant_cols = [ 
#     'median_household_income', 'percentage_female',
#     'percentage_age_over_65', 
#     'less_than_high_school_diploma',
#     'hispanic_latino', 'black_or_african_american_alone', 'asian_alone', 'white_alone'
# ]

# # Clean the data
# data = data.dropna(subset=relevant_cols + ['avg_d_mbps'])

# X = data[relevant_cols]
# y = data['avg_d_mbps']

# # Create interaction terms
# X.loc[:, 'income_female'] = X['median_household_income'] * X['percentage_female']
# X.loc[:, 'income_age_over_65'] = X['median_household_income'] * X['percentage_age_over_65']
# X.loc[:, 'income_hispanic'] = X['median_household_income'] * X['hispanic_latino']

# # Polynomial feature generation (degree 2)
# poly = PolynomialFeatures(degree=2, include_bias=False)
# X_poly = poly.fit_transform(X)

# # Get the feature names for the generated polynomial features
# poly_features = poly.get_feature_names_out(input_features=X.columns)

# # Define the relevant columns based on interaction terms and original features
# selected_columns = ['median_household_income', 'percentage_female', 'percentage_age_over_65', 
#                     'less_than_high_school_diploma', 'hispanic_latino', 'black_or_african_american_alone', 
#                     'asian_alone', 'white_alone', 'income_female', 'income_age_over_65', 'income_hispanic']

# # Ensure the selected columns are present in X_poly_df before filtering
# reduced_poly_features = [feature for feature in poly_features if feature in selected_columns]

# # Filter out only the relevant columns from the polynomial features
# X_poly_df = pd.DataFrame(X_poly, columns=poly_features)[reduced_poly_features]

# # Feature Scaling
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X_poly_df)

# # Train-test split
# X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# # Model 1: Random Forest
# rf = RandomForestRegressor(n_estimators=200, max_depth=20, min_samples_split=5, random_state=42)
# rf.fit(X_train, y_train)

# # Predict and evaluate Random Forest
# y_pred_rf = rf.predict(X_test)
# print("Random Forest R² Score:", r2_score(y_test, y_pred_rf))
# print("Random Forest MAE:", mean_absolute_error(y_test, y_pred_rf))
# print("Random Forest RMSE:", np.sqrt(mean_squared_error(y_test, y_pred_rf)))

# # Model 2: Gradient Boosting
# gb = GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=3, random_state=42)
# gb.fit(X_train, y_train)

# # Predict and evaluate Gradient Boosting
# y_pred_gb = gb.predict(X_test)
# print("Gradient Boosting R² Score:", r2_score(y_test, y_pred_gb))
# print("Gradient Boosting MAE:", mean_absolute_error(y_test, y_pred_gb))
# print("Gradient Boosting RMSE:", np.sqrt(mean_squared_error(y_test, y_pred_gb)))

# # Feature Importance for Random Forest
# feature_importance = rf.feature_importances_

# # Create DataFrame for feature importance
# importance_df = pd.DataFrame({'Feature': reduced_poly_features, 'Importance': feature_importance})

# # Print the feature importance DataFrame
# print("Feature Importance for Random Forest:")
# print(importance_df)

# # Optionally, save the feature importance to a CSV file
# # importance_df.to_csv('feature_importance.csv', sep=';', index=False)

import shap
import matplotlib.pyplot as plt

# Use your model and dataset
X = data[["median_household_income", "percentage_age_over_65", "less_than_high_school_diploma", 
          "hispanic_latino", "black_or_african_american_alone", "percentage_female", "asian_alone"]]
y = data["avg_d_mbps_mean"]

# Explainer for Random Forest
explainer = shap.Explainer(rf_model, X)
shap_values = explainer(X)

# SHAP Summary Plot
shap.summary_plot(shap_values, X)
