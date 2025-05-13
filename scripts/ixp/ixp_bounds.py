# This script calculates the latitude and longitude range values for a given position

import math

ixp_lat = 33.879828
ixp_lon = -118.026751
radius_km = 50

# latitude and longitude range
lat_range = radius_km / 111  # 1 degree latitude ~ 111 km
lon_range = radius_km / (111 * math.cos(math.radians(ixp_lat)))

# bounds
min_lat = ixp_lat - lat_range
max_lat = ixp_lat + lat_range
min_lon = ixp_lon - lon_range
max_lon = ixp_lon + lon_range

print(f"Latitude range: {min_lat} to {max_lat}")
print(f"Longitude range: {min_lon} to {max_lon}")