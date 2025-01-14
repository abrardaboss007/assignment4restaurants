# import pandas as pd
# import geopandas as gpd
# import streamlit as st
# import matplotlib.pyplot as plt
# import os
# import numpy as np
# from pyogrio import set_gdal_config_options

# set_gdal_config_options({
#     "SHAPE_RESTORE_SHX" : "YES",
# })
# # -----------------------------------------------------------------------------------------------------
# # Function to read the DataFrame from a CSV file
# def read_from_csv(filename="restaurant_data.csv"):
#     df_loaded = pd.read_csv(filename)
#     print(f"Data loaded from {filename}")
#     return df_loaded

# # Read the DataFrame back from the CSV
# df = read_from_csv("restaurant_data.csv")
# # -----------------------------------------------------------------------------------------------------
# # Create map of London using shapefiles
# df["RatingValue"] = df["RatingValue"].astype(int)
# london_boroughs = df["LocalAuthorityName"].unique().tolist()

# # Initialise an empty list to store GeoDataFrames
# gdfs = []

# # Iterate through each borough and load the shapefile
# for borough in london_boroughs:
#     fp = os.path.join("shapefiles", f"{borough}.shp")  
#     map_df = gpd.read_file(fp)
    
#     # Add the GeoDataFrame to the list
#     gdfs.append(map_df)

# # Combine all GeoDataFrames into a single GeoDataFrame
# combined_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))
# # -----------------------------------------------------------------------------------------------------
# # Calculate mean hygiene rating for each borough
# mean_hygiene_rating_list = []
# for borough in london_boroughs:
#     borough_df = df[df["LocalAuthorityName"].isin([borough])]
#     mean = borough_df["RatingValue"].mean()
#     mean_hygiene_rating_list.append(mean)
# mean_hygiene_rating_list = np.array(mean_hygiene_rating_list).tolist()

# list_of_borough_indices = []
# for borough in london_boroughs:
#     first_occurence_of_borough_index = df[df.LocalAuthorityName == borough].first_valid_index()
#     list_of_borough_indices.append(first_occurence_of_borough_index)
# list_of_borough_indices = np.array(list_of_borough_indices).tolist()

# df1 = df.iloc[list_of_borough_indices,:]
# df1["AverageHygiene"] = mean_hygiene_rating_list
# # ---------------------------------------------------------------------------------------
# # Join the dataframes
# merged = combined_gdf.set_index("lad22nm").join(df1.set_index("LocalAuthorityName"))
# # -------------------------------------------------------------------------------------------
# # Final touches to heatmap for visualisation purposes
# variable = "AverageHygiene"

# vmin, vmax = 1,5

# fig, ax = plt.subplots(1, figsize=(10, 6))
# merged.plot(column=variable, cmap="Blues", linewidth=0.8, ax=ax, edgecolor=None)
# ax.axis("off")
# ax.set_title("Average hygiene ratings for London Boroughs", fontsize=16)
# # Create colorbar as a legend
# sm = plt.cm.ScalarMappable(cmap="Blues", norm=plt.Normalize(vmin=vmin, vmax=vmax))
# # empty array for the data range
# sm._A = []
# # add the colorbar to the figure
# cbar = fig.colorbar(sm, ax=ax)
# st.pyplot(fig=fig)
# #----------------------------------------------------------------------------------------------
# # Creating bar chart for top right of dashboard
# restaurant_df = df[df["BusinessType"] == "Restaurant/Cafe/Canteen"]
# takeaway_df = df[df["BusinessType"]== "Takeaway/sandwich shop"]

# number_of_restaurants = len(restaurant_df)
# number_of_takeaways = len(takeaway_df)


# comparison_data = {
#     "Establishment Type":["Restaurant/Cafe/Canteen","Takeaway/Sandwich Shop"],
#     "Number of Establishments":[number_of_restaurants,number_of_takeaways]
# }

# comparison_data = pd.DataFrame(comparison_data)

# st.write(comparison_data)

# st.bar_chart(comparison_data, x = "Establishment Type", y="Number of Establishments", width = 300, height = 500)
# # --------------------------------------------------------------------------------------------------------
# # Creating line graph for bottom left
# # number_of_establishments_per_borough = []
# # for borough in london_boroughs:
# #     df2 = df[df["LocalAuthorityName"] == borough]
# #     length = len(df2)
# #     number_of_establishments_per_borough.append(length)
# # print(number_of_establishments_per_borough)

# # Import necessary libraries
# from datetime import datetime
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import r2_score
# import seaborn as sns

# class LineGraph:
#     def __init__(self, df):
#         self.df = df.copy()
#         self.borough_data = None
#         self.r_squared = None

#     def preprocess_data(self):
#         # Calculate days since last hygiene score update
#         self.df["RatingDate"] = pd.to_datetime(self.df["RatingDate"], errors="coerce")
#         self.df["DaysSinceLastUpdate"] = (datetime.today() - self.df["RatingDate"]).dt.days

#         # Group by borough
#         self.borough_data = self.df.groupby("LocalAuthorityName").agg({
#             "BusinessName": "count",  # Total establishments
#             "DaysSinceLastUpdate": "mean",  # Mean days since last update
#         }).reset_index()

#         # Rename columns for clarity
#         self.borough_data.columns = ["Borough", "NumberOfEstablishments", "MeanDaysSinceUpdate"]

#     def calculate_regression_and_r2(self):
#         # Extract X and Y
#         X = self.borough_data["NumberOfEstablishments"].values.reshape(-1, 1)
#         y = self.borough_data["MeanDaysSinceUpdate"].values

#         # Perform linear regression
#         model = LinearRegression()
#         model.fit(X, y)
#         y_pred = model.predict(X)

#         # Calculate R²
#         self.r_squared = r2_score(y, y_pred)

#     def plot_regression_line(self):
#         # Calculate regression and R²
#         self.calculate_regression_and_r2()

#         # Plot regression with Seaborn
#         fig, ax = plt.subplots(figsize=(10, 6))
#         sns.regplot(
#             data=self.borough_data,
#             x="NumberOfEstablishments",
#             y="MeanDaysSinceUpdate",
#             ax=ax,
#             scatter_kws={"s": 50},  # Adjust marker size
#             line_kws={"color": "red", "label": f"R² = {self.r_squared:.2f}"}
#         )

#         # Add labels, title, and legend
#         ax.set_title("Number of Establishments in Each London Borough against Mean Days Elapsed Since Last Update")
#         ax.set_xlabel("Number of Establishments in Each London Borough")
#         ax.set_ylabel("Mean Number of Days Elapsed Since Last Update")
#         ax.legend(loc="upper right")
#         ax.grid(True)

#         # Display the graph in Streamlit
#         st.pyplot(fig=fig)

# # Initialize and process data for the regression line graph
# line_graph = LineGraph(df)
# line_graph.preprocess_data()

# # Display the regression line graph
# line_graph.plot_regression_line()

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
st.title("London Food Establishment Dashboard")

# Create a layout with four sections
col1, col2 = st.columns(2)
with col1:
    with st.container(border = True, height=300):
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
    with st.container(border = True, height=300):
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
    with st.container(border = True, height=300):
        st.pyplot(line_graph.plot_regression_line())

with col4:
    with st.container(border = True, height=300):
        st.markdown("""
            - **Heatmap:** Shows the average hygiene ratings across different London boroughs.
            - **Bar Chart:** Compares the number of restaurants versus takeaways in London.
            - **Regression Line:** Examines the relationship between the number of establishments and the mean days since their last update.
            - You can replace this placeholder text with your own analysis or insights.
        """)
