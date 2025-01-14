# import time
# from datetime import datetime

# def difference_in_dates(todays_date(), date1):
#     def todays_date():
#         today = datetime.today()
#         formatted_today = today.strftime("%d/%m/%Y")
#         return formatted_today
#     date_format = "%d/%m/%Y"
#     a = time.mktime(time.strptime(date1, date_format))
#     delta = abs(formatted_today - a)
#     return int(delta / 86400)


# def todays_date():
#     today = datetime.today()
#     formatted_today = today.strftime("%d/%m/%Y")
#     return formatted_today

# print(difference_in_dates(todays_date(),"18/04/2005"))


# Function to read the DataFrame from a CSV file
import random
import pandas as pd
import geopandas as gpd
import streamlit as st
import matplotlib.pyplot as plt
import os
import numpy as np

def read_from_csv(filename="restaurant_data.csv"):
    df_loaded = pd.read_csv(filename, usecols=[3,6])
    print(f"Data loaded from {filename}")
    return df_loaded

# Read the DataFrame back from the CSV
df = read_from_csv("restaurant_data.csv")

london_boroughs = list(df["LocalAuthorityName"].unique())
df["RatingValue"] = df["RatingValue"].astype(int)


empty_list = []
for borough in london_boroughs:
    borough_df = df[df["LocalAuthorityName"].isin([borough])]
    mean = borough_df["RatingValue"].mean()
    empty_list.append(mean)
empty_list = np.array(empty_list).tolist()

list_of_borough_indices = []
for borough in london_boroughs:
    first_occurence_of_borough_index = df[df.LocalAuthorityName == borough].first_valid_index()
    list_of_borough_indices.append(first_occurence_of_borough_index)

list_of_borough_indices = np.array(list_of_borough_indices).tolist()
print(list_of_borough_indices)

df = df.iloc[list_of_borough_indices,:]
df["AverageHygiene"] = empty_list
print(df)

# a =df.loc[indec-1,"LocalAuthorityName"]
# b = df.loc[indec,"LocalAuthorityName"]

# i = 0
# for borough in london_boroughs:
#     print(f"{borough} has an average hygiene rating of {empty_list[i]}")
#     i += 1