import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
import time

# Function to create density bins based on standard deviation
def create_density_bins(data, column='population_density', num_bins=3):
    # Create the density bins using qcut: (quantile-based discretization) from pandas
    data['Density_Bucket'] = pd.qcut(data[column], q=num_bins, labels=[f'Bin_{i+1}' for i in range(num_bins)], duplicates='drop')
    
    # Get bin ranges from qcut's output (bin_edges gives the actual numeric edges of the bins)
    bin_ranges = pd.qcut(data[column], q=num_bins, labels=False, retbins=True)[1]
    
    for i in range(1, num_bins+1):
        bin_range = (bin_ranges[i-1], bin_ranges[i])
        bin_count = data[data['Density_Bucket'] == f'Bin_{i}'].shape[0]
        print(f'Bin {i}: Count: {bin_count} : {bin_range[0]} to {bin_range[1]}')
    
    return data

# Function to train Random Forest model and calculate feature importance
def train_rf_model(X_train, y_train, X_test, y_test, relevant_cols):
    rf = RandomForestRegressor(n_estimators=200, max_depth=20, min_samples_split=5, random_state=42)
    rf.fit(X_train, y_train)
    
    feature_importance = rf.feature_importances_
    importance_df = pd.DataFrame({'Feature': relevant_cols, 'Importance': feature_importance}).sort_values(by='Importance', ascending=False)
    
    y_pred = rf.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    return rf, importance_df, y_pred, r2, mae, rmse

# Function to add correlation column for direction of feature importance
def direct_correlation(X, y):
    correlation = X.corrwith(y)
    correlation_df = pd.DataFrame({'Feature': relevant_cols, 'Correlation': correlation})
    
    return correlation_df

# Function to calculate permutation importance
def calculate_permutation_importance(rf, X_test, y_test, relevant_cols):
    perm_importance = permutation_importance(rf, X_test, y_test, n_repeats=10, random_state=42)
    permutation_df = pd.DataFrame({
        'Feature': relevant_cols,
        'Permutation Importance': perm_importance.importances_mean
    }).sort_values(by='Permutation Importance', ascending=False)
    
    return permutation_df

# def evaluate_permutation_importance(rf, X_test, y_test, relevant_cols):
#     baseline_r2 = r2_score(y_test, rf.predict(X_test))
#     baseline_mae = mean_absolute_error(y_test, rf.predict(X_test))
#     baseline_rmse = np.sqrt(mean_squared_error(y_test, rf.predict(X_test)))
    
#     perm_importance = permutation_importance(rf, X_test, y_test, n_repeats=10, random_state=42)
    
#     # Track the performance degradation for each feature
#     performance_degradation = {}
#     for idx, feature in enumerate(relevant_cols):
#         # Shuffle the feature and calculate performance degradation
#         X_test_permuted = X_test.copy()
#         X_test_permuted[:, idx] = np.random.permutation(X_test_permuted[:, idx])  # Shuffle feature
        
#         # Calculate new performance after permutation
#         perm_r2 = r2_score(y_test, rf.predict(X_test_permuted))
#         perm_mae = mean_absolute_error(y_test, rf.predict(X_test_permuted))
#         perm_rmse = np.sqrt(mean_squared_error(y_test, rf.predict(X_test_permuted)))
        
#         # Calculate performance degradation
#         performance_degradation[feature] = {
#             'R² Degradation': baseline_r2 - perm_r2,
#             'MAE Degradation': perm_mae - baseline_mae,
#             'RMSE Degradation': perm_rmse - baseline_rmse
#         }
        
#     return performance_degradation, perm_importance.importances_mean


# Function to calculate null model importance
def calculate_null_model_importance(rf, X_test, y_test, relevant_cols):
    y_test_array = np.array(y_test)
    np.random.shuffle(y_test_array)
    result_null = permutation_importance(rf, X_test, y_test_array, n_repeats=10, random_state=42)
    
    null_importance_df = pd.DataFrame({
        'Feature': relevant_cols,
        'Null Model Importance': result_null.importances_mean
    }).sort_values(by='Null Model Importance', ascending=False)
    
    return null_importance_df

# Main function to process the dataset, train the model, and evaluate
def run_random_forest_model(data, relevant_cols, dependent_col):
    start_time = time.time()
    
    data = create_density_bins(data)
    
    results = []
    
    for label in ['Bin_1', 'Bin_2', 'Bin_3']:
        subset_data = data[data['Density_Bucket'] == label]
        subset_data = subset_data.dropna(subset=relevant_cols + [dependent_col])
        
        if subset_data.empty:
            print(f"No data available for {label} density bucket.")
            continue
        
        X = subset_data[relevant_cols]
        y = subset_data[dependent_col]
        
        # Scale the features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # split the data into test and train
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.4, random_state=42)
        
        rf, result_importance, y_pred, r2, mae, rmse = train_rf_model(X_train, y_train, X_test, y_test, relevant_cols)
        
        # find the correlation of features with the target for direction
        correlation_df = direct_correlation(X, y)

        # merge the feature importance and correlation
        imp_corr_df = pd.merge(result_importance, correlation_df, on='Feature')

        # calculate permutation importance for validation
        permutation_df = calculate_permutation_importance(rf, X_test, y_test, relevant_cols)
        
        # print(f"Permutation Importance and Performance Degradation for {label}:")
        # print("Feature Performance Degradation (R², MAE, RMSE):")
        # for feature, degradation in performance_degradation.items():
        #     print(f"{feature}: {degradation}")

        # calculate null model importance for validation
        null_importance_df = calculate_null_model_importance(rf, X_test, y_test, relevant_cols)
        null_importance_df = pd.DataFrame(null_importance_df)

        # merge the permutation importance and null model importance
        permutation_result_df = pd.merge(permutation_df, null_importance_df, on='Feature')

        # merge the permutation importance and null model importance with the feature importance and correlation
        result_df = pd.merge(imp_corr_df, permutation_result_df, on='Feature').sort_values(by='Permutation Importance', ascending=False)
        
        results.append({
            'Density_Bucket': label,
            'R²': r2,
            'MAE': mae,
            'RMSE': rmse,
            'Result Table': result_df
        })
        
        print(f"Results for {dependent_col} in {label} Population Density Bucket:")
        print(f"R² Score: {r2}")
        print(f"MAE: {mae}")
        print(f"RMSE: {rmse}")
        print(result_df)
        print("-" * 50)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total Time (s): {elapsed_time:.2f}")
    
    return results

file_paths = {
    'california': "../../../../../results/ookla/US/cbg/raw_masters/state_master_fixed_06.csv",

    'elnorte': "../../../../../results/ookla/US/cbg/raw_masters/nation_master_fixed_06_EL NORTE.csv",
    'thefarwest': "../../../../../results/ookla/US/cbg/raw_masters/nation_master_fixed_06_THE FAR WEST.csv",
    'theleftcoast': "../../../../../results/ookla/US/cbg/raw_masters/nation_master_fixed_06_THE LEFT COAST.csv",

    'elnorte_ventura': "../../../../../results/ookla/US/cbg/raw_census/ookla_fixed_cbg_06_111_census.csv",
    'thefarwest_fresno': "../../../../../results/ookla/US/cbg/raw_census/ookla_fixed_cbg_06_019_census.csv",
    'theleftcoast_santaclara': "../../../../../results/ookla/US/cbg/raw_census/ookla_fixed_cbg_06_085_census.csv",

    # aggregated
    'bayarea': "../../../../../results/ookla/US/cbg/masters/ookla_fixed_cbg_master_06_bayarea.csv",

    'middlecalifornia': "../../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_06_middlecalifornia.csv",
    'losangelesarea': "../../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_06_losangelesarea.csv",
    'dallasarea': "../../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_48_dallasarea.csv",
    'houstonarea': "../../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_48_houstonarea.csv",
    'southtexasarea': "../../../../../results/ookla/US/cbg/raw_masters/ookla_fixed_cbg_master_48_southtexasarea.csv",
}

file_path = file_paths['bayarea']

data = pd.read_csv(file_path, low_memory=False)

relevant_cols = [
    'median_household_income', 'percentage_female',
    'percentage_age_over_65', 
    'less_than_high_school_diploma',
    'hispanic_latino', 'black_or_african_american_alone', 'asian_alone'
]

dependent_col = 'avg_d_mbps_mean'
# dependent_col = 'avg_u_mbps'
# dependent_col = 'avg_lat_ms'

results = run_random_forest_model(data, relevant_cols, dependent_col)

pd.DataFrame(results).to_csv('results_per_density_bucket.csv', index=False)
