import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

file_path = file_paths['elnorte']

data = pd.read_csv(file_path, low_memory=False)

plt.figure(figsize=(8, 6))
# plt.scatter(data['population_density'], data['avg_d_mbps'], alpha=0.6, color='blue')
sns.regplot(x='hispanic_latino', y='avg_d_mbps', data=data, scatter_kws={'alpha': 0.6}, line_kws={'color': 'black'})


plt.xlabel('Population Density', fontsize=12)
plt.ylabel('Download Speed (Mbps)', fontsize=12)
plt.title('Download Speed vs Population Density', fontsize=14)
plt.grid(True)

plt.show()