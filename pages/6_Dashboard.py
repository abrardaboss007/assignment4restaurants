import pandas as pd
import geopandas as gpd
import streamlit as st
import matplotlib.pyplot as plt
import os
import numpy as np
from pyogrio import set_gdal_config_options
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import seaborn as sns
# Set GDAL config options
set_gdal_config_options({
    "SHAPE_RESTORE_SHX": "YES",
})
# Function to read the DataFrame from a CSV file
def read_from_csv(filename="restaurant_data.csv"):
    df_loaded = pd.read_csv(filename)
    print(f"Data loaded from {filename}")
    return df_loaded
# Read the DataFrame back from the CSV
df = read_from_csv("restaurant_data.csv")

# Create map of London using shapefiles
df["RatingValue"] = df["RatingValue"].astype(int)
london_boroughs = df["LocalAuthorityName"].unique().tolist()

# Initialise an empty list to store GeoDataFrames
gdfs = []
for borough in london_boroughs:
    fp = os.path.join("shapefiles", f"{borough}.shp")  
    map_df = gpd.read_file(fp)
    gdfs.append(map_df)

# Combine all GeoDataFrames into a single GeoDataFrame
combined_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))

# Calculate mean hygiene rating for each borough
mean_hygiene_rating_list = []
for borough in london_boroughs:
    borough_df = df[df["LocalAuthorityName"].isin([borough])]
    mean = borough_df["RatingValue"].mean()
    mean_hygiene_rating_list.append(mean)

list_of_borough_indices = []
for borough in london_boroughs:
    first_occurence_of_borough_index = df[df.LocalAuthorityName == borough].first_valid_index()
    list_of_borough_indices.append(first_occurence_of_borough_index)

df1 = df.iloc[list_of_borough_indices, :]
df1["AverageHygiene"] = mean_hygiene_rating_list

# Join the dataframes
merged = combined_gdf.set_index("lad22nm").join(df1.set_index("LocalAuthorityName"))

# Class for the regression line graph
class LineGraph:
    def __init__(self, df):
        self.df = df.copy()
        self.borough_data = None
        self.r_squared = None

    def preprocess_data(self):
        self.df["RatingDate"] = pd.to_datetime(self.df["RatingDate"], errors="coerce")
        self.df["DaysSinceLastUpdate"] = (datetime.today() - self.df["RatingDate"]).dt.days
        self.borough_data = self.df.groupby("LocalAuthorityName").agg({
            "BusinessName": "count",
            "DaysSinceLastUpdate": "mean",
        }).reset_index()
        self.borough_data.columns = ["Borough", "NumberOfEstablishments", "MeanDaysSinceUpdate"]

    def calculate_regression_and_r2(self):
        X = self.borough_data["NumberOfEstablishments"].values.reshape(-1, 1)
        y = self.borough_data["MeanDaysSinceUpdate"].values
        model = LinearRegression()
        model.fit(X, y)
        self.r_squared = r2_score(y, model.predict(X))

    def plot_regression_line(self):
        self.calculate_regression_and_r2()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.regplot(
            data=self.borough_data,
            x="NumberOfEstablishments",
            y="MeanDaysSinceUpdate",
            ax=ax,
            scatter_kws={"s": 50},
            line_kws={"color": "red", "label": f"R² = {self.r_squared:.2f}"}
        )
        ax.set_title("Number of Establishments vs. Mean Days Since Last Update")
        ax.set_xlabel("Number of Establishments")
        ax.set_ylabel("Mean Days Since Last Update")
        ax.legend(loc="upper right")
        return fig

# Initialize and preprocess data for regression line graph
line_graph = LineGraph(df)
line_graph.preprocess_data()

# Creating the dashboard layout
st.title("Food Establishment Dashboard")

# Create a layout with four sections
col1, col2 = st.columns(2)
with col1:
    with st.container(border = True, height=350):
        # Create heatmap
        fig, ax = plt.subplots(figsize=(8, 6))
        merged.plot(column="AverageHygiene", cmap="Blues", linewidth=0.8, ax=ax, edgecolor=None)
        ax.axis("off")
        ax.set_title("Average Hygiene Ratings for London Boroughs", fontsize=16)
        sm = plt.cm.ScalarMappable(cmap="Blues", norm=plt.Normalize(vmin=1, vmax=5))
        sm._A = []
        fig.colorbar(sm, ax=ax)
        st.pyplot(fig)

with col2:
    with st.container(border = True, height=350):
        # Create bar chart
        restaurant_df = df[df["BusinessType"] == "Restaurant/Cafe/Canteen"]
        takeaway_df = df[df["BusinessType"] == "Takeaway/sandwich shop"]
        comparison_data = pd.DataFrame({
            "Establishment Type": ["Restaurant/Cafe/Canteen", "Takeaway/Sandwich Shop"],
            "Number of Establishments": [len(restaurant_df), len(takeaway_df)]
        })
        st.bar_chart(comparison_data, x = "Establishment Type", y="Number of Establishments", width = 170, height = 275)

col3, col4 = st.columns(2)
with col3:
    with st.container(border = True, height=350):
        st.pyplot(line_graph.plot_regression_line())

with col4:
    with st.container(border = True, height=350):
        st.markdown("""
            - **Heatmap:** Shows that boroughs in the middle and south of London have higher average ratings that boroughs in the north.
            - **Bar Chart:** Restaurants/Cafe/Canteen establishments are almost three times as prevalent as Takeaway/Sandwich shop establishments.
            - **Regression Line:** There is no linear correlation with the number of establishments in a borough and the average time elapsed since those establishments were hygiene reviewed.

        """)
