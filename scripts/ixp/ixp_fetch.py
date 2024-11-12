import requests
import pandas as pd

# Fetch IXP data
ixp_response = requests.get("https://www.peeringdb.com/api/ix?country=US")
ixp_data = ixp_response.json().get("data", [])

# Fetch facility data associated with IXPs
facilities_response = requests.get("https://www.peeringdb.com/api/fac?country=US")
facilities_data = facilities_response.json().get("data", [])

# Create DataFrames for analysis
ixp_df = pd.DataFrame(ixp_data)
facilities_df = pd.DataFrame(facilities_data)

# Save data to CSV for later analysis
ixp_df.to_csv("ixp_data.csv", index=False)
facilities_df.to_csv("facilities_data.csv", index=False)

print("Data has been saved to CSV.")
