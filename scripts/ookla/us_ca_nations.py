import pandas as pd

input_file= f"../../../datasets/census/US/regions/woodard_countywise.csv"
output_file= f"../../../datasets/census/US/regions/woodard_countywise_california.csv"

df = pd.read_csv(input_file)

california_rows = df[df['STATE NAME'] == 'California']

# Save the filtered DataFrame to a new CSV file
california_rows.to_csv(output_file, index=False)

print(f"Filtered rows saved to: {output_file}")