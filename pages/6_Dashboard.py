import pandas as pd
import geopandas as gpd
import streamlit as st
import matplotlib.pyplot as plt
import os
from pyogrio import set_gdal_config_options

set_gdal_config_options({
    "SHAPE_RESTORE_SHX" : "YES",
})
# -----------------------------------------------------------------------------------------------------
# Function to read the DataFrame from a CSV file
#@st.cache_data
def read_from_csv(filename="restaurant_data.csv"):
    df_loaded = pd.read_csv(filename)
    print(f"Data loaded from {filename}")
    return df_loaded

# Read the DataFrame back from the CSV
df = read_from_csv("restaurant_data.csv")
# -----------------------------------------------------------------------------------------------------
# Create map of London using shapefiles
df["RatingValue"] = df["RatingValue"].astype(int)
london_boroughs = df["LocalAuthorityName"].unique().tolist()

# Initialise an empty list to store GeoDataFrames
gdfs = []

# Iterate through each borough and load the shapefile
for borough in london_boroughs:
    fp = os.path.join("shapefiles", f"{borough}.shp")  
    map_df = gpd.read_file(fp)
    
    # Add the GeoDataFrame to the list
    gdfs.append(map_df)

# Combine all GeoDataFrames into a single GeoDataFrame
combined_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))

# Plot the combined GeoDataFrame
fig, ax = plt.subplots(1, 1, figsize=(12, 10))
combined_gdf.plot(ax=ax, color="lightblue", edgecolor=None)
ax.set_title("London Boroughs", fontsize=16)
#plt.show()
# -----------------------------------------------------------------------------------------------------
st.write(combined_gdf)