import geopandas as gpd
import matplotlib.pyplot as plt

gpkg_file = 'my_file.gpkg' 
gdf = gpd.read_file(gpkg_file)

print(gdf.head())

output = 'my_geofile.csv'
gdf.to_csv(output, index=False)

# gdf.plot(column='your_column',
#           cmap='viridis', 
#           legend=True,
#           figsize=(10, 10))

# plt.title('Plot of GeoPackage Data')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')

# plt.show()