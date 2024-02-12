import requests
import os

# Base URL of the directory
url = 'https://publicdata.caida.org/datasets/ixps/'

# List of known or discovered JSON and JSONL file names
# ixs_files = [
#     "ixs_201802.jsonl",
#     "ixs_201807.jsonl",         
#     "ixs_201810.jsonl",          
#     "ixs_201901.jsonl",           
#     "ixs_201904.jsonl",           
#     "ixs_201907.jsonl",           
#     "ixs_201910.jsonl",            
#     "ixs_202001.jsonl",           
#     "ixs_202004.jsonl",        
#     "ixs_202007.jsonl",           
#     "ixs_202010.jsonl",     
#     "ixs_202101.jsonl",         
#     "ixs_202104.jsonl",          
#     "ixs_202107.jsonl",      
#     "ixs_202110.jsonl",     
#     "ixs_202201.jsonl",     
#     "ixs_202204.jsonl",          
#     "ixs_202207.jsonl",    
#     "ixs_202210.jsonl",      
#     "ixs_202301.jsonl",       
#     "ixs_202304.jsonl",      
#     "ixs_202307.jsonl",           
#     "ixs_202310.jsonl",           
#     "ixs_202401.jsonl"
# ]

# facilities_files = [
#     "facilities_201802.jsonl",
#     "facilities_201807.jsonl",
#     "facilities_201810.jsonl",
#     "facilities_201901.jsonl",
#     "facilities_201904.jsonl",
#     "facilities_201907.jsonl",
#     "facilities_201910.jsonl",
#     "facilities_202001.jsonl",
#     "facilities_202004.jsonl",
#     "facilities_202007.jsonl",
#     "facilities_202010.jsonl",
#     "facilities_202101.jsonl",
#     "facilities_202104.jsonl",
#     "facilities_202107.jsonl",
#     "facilities_202110.jsonl",
#     "facilities_202201.jsonl",
#     "facilities_202204.jsonl",
#     "facilities_202207.jsonl",
#     "facilities_202210.jsonl",
#     "facilities_202301.jsonl",
#     "facilities_202304.jsonl",
#     "facilities_202307.jsonl",
#     "facilities_202310.jsonl",
#     "facilities_202401.jsonl"
# ]

locations_files = [
    "locations_201802.jsonl",
    "locations_201807.jsonl",
    "locations_201810.jsonl",
    "locations_201901.jsonl",
    "locations_201904.jsonl",
    "locations_201907.jsonl",
    "locations_201910.jsonl",
    "locations_202001.jsonl",
    "locations_202004.jsonl",
    "locations_202007.jsonl",
    "locations_202010.jsonl",
    "locations_202101.jsonl",
    "locations_202104.jsonl",
    "locations_202107.jsonl",
    "locations_202110.jsonl",
    "locations_202201.jsonl",
    "locations_202204.jsonl",
    "locations_202207.jsonl",
    "locations_202210.jsonl",
    "locations_202301.jsonl",
    "locations_202304.jsonl",
    "locations_202307.jsonl",
    "locations_202310.jsonl",
    "locations_202401.jsonl"
]

# Directory to save downloaded files
download_dir = "/Users/beja/Desktop/Classes/Winter'24/project/Internet-Access-Disparities/datasets/IXP/locations dataset"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

for file_name in locations_files:
    file_url = url + file_name
    response = requests.get(file_url)
    if response.status_code == 200:
        file_path = os.path.join(download_dir, file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'Downloaded {file_name}')
    else:
        print(f'Failed to download {file_name}')

print('All files downloaded.')
