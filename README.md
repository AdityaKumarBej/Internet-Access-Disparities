# Internet-Access-Disparities
Internet Access Disparities


# IXP Datasets
CAID Dataset - https://publicdata.caida.org/datasets/ixps/

File ixs.jsonl contains information about individual IXPs. The "pch_id", "pdb_id", and "pdb_org_id" values match the IXP ids in the original sources, Packet Clearing House (PCH) and PeeringDB (PDB) respectively. Other fields are self-explanatory.

File organizations.jsonl contains the information about each organization learned from PDB. These can be matched with their corresponding facility by matching the facility's pdb_org_id with the organization's pdb_org_id.

File locations.jsonl is similar to the geoname locations, but contains negative "geo_id"s for those locations where geographic locations of IXPs were not found in the geonames dataset.

# Ookla Datasets
TIGER (Topologically Integrated Geographic Encoding and Referencing) shapefiles are a type of digital data produced by the United States Census Bureau. They contain detailed geographic and cartographic information used for mapping and geographic analysis. TIGER shapefiles are an integral part of the infrastructure for mapping and geographic information systems (GIS) in the United States, supporting various applications, including demographics, urban planning, transportation, and more.

STATEEFP for mapping in Ookla:
Alabama: 01
Alaska: 02
Arizona: 04
Arkansas: 05
California: 06
Colorado: 08
Connecticut: 09
Delaware: 10
Florida: 12
Georgia: 13
Hawaii: 15
Idaho: 16
Illinois: 17
Indiana: 18
Iowa: 19
Kansas: 20
Kentucky: 21
Louisiana: 22
Maine: 23
Maryland: 24
Massachusetts: 25
Michigan: 26
Minnesota: 27
Mississippi: 28
Missouri: 29
Montana: 30
Nebraska: 31
Nevada: 32
New Hampshire: 33
New Jersey: 34
New Mexico: 35
New York: 36
North Carolina: 37
North Dakota: 38
Ohio: 39
Oklahoma: 40
Oregon: 41
Pennsylvania: 42
Rhode Island: 44
South Carolina: 45
South Dakota: 46
Tennessee: 47
Texas: 48
Utah: 49
Vermont: 50
Virginia: 51
Washington: 53
West Virginia: 54
Wisconsin: 55
Wyoming: 56
District of Columbia: 11

# M-LAB dataset
M-LAB hosts it's network data in a custom BigQuery link - https://www.measurementlab.net/data/docs/bq/quickstart/

# geo spatial data for the rest of the world
https://gadm.org/data.html