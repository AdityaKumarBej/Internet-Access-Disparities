import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from scipy.stats import zscore

data = pd.read_csv("../../../../results/ookla/US/cbg/masters/ookla_fixed_cbg_master_06_middlecaliforniaarea.csv", low_memory=False)

relevant_cols = ['total_tests', 'total_devices', 
    'population_density', 'median_household_income',
    'percentage_age_under_5', 'percentage_age_5_17', 'percentage_age_18_64', 'percentage_age_over_65',
    'percentage_male', 'percentage_female',
    'less_than_high_school_diploma', 'high_school_diploma_only', 'bachelor_or_associate_degree' ,'masters_or_more',
    'hispanic_latino', 'white_alone', 'black_or_african_american_alone', 'american_indian_and_alaskan_native_alone', 'asian_alone', 'native_hawaiian_and_other_pacific_islander_alone', 'two_or_more_races', 'some_other_race_alone'
]

data = data.dropna(subset=relevant_cols)

data = data[(np.abs(zscore(data[relevant_cols])) < 3).all(axis=1)]

x = data[relevant_cols]
y = data['avg_d_mbps_mean']

scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

####### IMP IMP
pd.options.display.float_format = '{:.10f}'.format 

print(f'Mean Squared Error: {mse}')
print(f'R² Score: {r2}')

coefficients = pd.DataFrame(model.coef_, columns=['Coefficient'], index=relevant_cols)
print(coefficients)

from statsmodels.stats.outliers_influence import variance_inflation_factor

vif_data = pd.DataFrame()
vif_data['Feature'] = x.columns
vif_data['VIF'] = [variance_inflation_factor(x.values, i) for i in range(x.shape[1])]
print(vif_data)
