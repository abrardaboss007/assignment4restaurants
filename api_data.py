import pandas as pd, geopandas as gpd, streamlit as st, os
# -----------------------------------------------------------------------------------------------------
#Loading up xml data into desired format using pandas dataframes
# PLEASE ALLOW UPTO 90 SECONDS FOR THIS CODE TO RUN
df1 = pd.read_xml("https://ratings.food.gov.uk/api/open-data-files/FHRS501en-GB.xml",
                xpath="/FHRSEstablishment/EstablishmentCollection/EstablishmentDetail")

df2 = pd.read_xml("https://ratings.food.gov.uk/api/open-data-files/FHRS501en-GB.xml",
                xpath="/FHRSEstablishment/EstablishmentCollection/EstablishmentDetail/Geocode")

df1 = df1[["BusinessName","BusinessType","PostCode","RatingValue","RatingKey","RatingDate","LocalAuthorityName"]]

url = "502"
for i in range(1,33):
    df3 = pd.read_xml(f"https://ratings.food.gov.uk/api/open-data-files/FHRS{url}en-GB.xml",
                      xpath="/FHRSEstablishment/EstablishmentCollection/EstablishmentDetail")
    df3 = df3[["BusinessName","BusinessType","PostCode","RatingValue","RatingKey","RatingDate","LocalAuthorityName"]]
    df4 = pd.read_xml(f"https://ratings.food.gov.uk/api/open-data-files/FHRS{url}en-GB.xml",
                xpath="/FHRSEstablishment/EstablishmentCollection/EstablishmentDetail/Geocode")
    df1 = pd.concat([df1, df3], axis=0)
    df2 = pd.concat([df2, df4], axis=0)
    url = str(int(url) + 1)

df = pd.concat([df1,df2], axis = 1)

df = df.dropna(subset = ["Postcode","RatingDate","Longitude","Latitude"])
df = df[df["BusinessType"].isin(["Restaurant/Cafe/Canteen", "Takeaway/sandwich shop"])]
pd.set_option('display.max_columns', None)

london_boroughs = list(df["LocalAuthorityName"].unique())
# -----------------------------------------------------------------------------------------------------
# Function to add image paths based on RatingKey
def add_image_paths(df, image_folder= r"images\test"):
    df["ImagePath"] = df["RatingKey"].apply(lambda key: os.path.join(image_folder, f"{key}.png"))
    return df
# -----------------------------------------------------------------------------------------------------
# Add image paths to the DataFrame
df = add_image_paths(df)
# -----------------------------------------------------------------------------------------------------
# Save the DataFrame to a CSV file
def save_to_csv(df, filename="restaurant_data.csv"):
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
# Save the updated DataFrame to a CSV
save_to_csv(df, "restaurant_data.csv")
# -----------------------------------------------------------------------------------------------------
