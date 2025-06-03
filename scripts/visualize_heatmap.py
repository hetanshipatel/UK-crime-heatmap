# scripts/visualize_heatmap.py

import pandas as pd
import folium
from folium.plugins import HeatMap
import os

# Load cleaned data
csv_path = os.path.join("data", "uk_crime_cleaned.csv")
df = pd.read_csv(csv_path)

# Check and fix column names if necessary
if "location.latitude" in df.columns and "location.longitude" in df.columns:
    lat_col = "location.latitude"
    lon_col = "location.longitude"
elif "latitude" in df.columns and "longitude" in df.columns:
    lat_col = "latitude"
    lon_col = "longitude"
else:
    raise KeyError("Latitude and longitude columns not found in the CSV file.")

# Drop rows with missing coordinates
df = df.dropna(subset=[lat_col, lon_col])
df[lat_col] = df[lat_col].astype(float)
df[lon_col] = df[lon_col].astype(float)

# Prepare data for heatmap
heat_data = df[[lat_col, lon_col]].values.tolist()

# Create base map centered around London
map_center = [51.509865, -0.118092]  # London coordinates
base_map = folium.Map(location=map_center, zoom_start=6, tiles="CartoDB dark_matter")

# Add heatmap
HeatMap(heat_data, radius=10, blur=15).add_to(base_map)

# Save map to HTML
output_path = os.path.join("output", "crime_heatmap.html")
os.makedirs("output", exist_ok=True)
base_map.save(output_path)

print(f"✅ Heatmap saved to '{output_path}'")
print(f"📍 Total plotted points: {len(heat_data)}")
