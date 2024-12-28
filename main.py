import pandas as pd, geopandas as gpd, streamlit as st
# ----------------------------------------------------------------------------------------------------------------------
df1 = pd.read_xml("https://ratings.food.gov.uk/api/open-data-files/FHRS501en-GB.xml",
                xpath="/FHRSEstablishment/EstablishmentCollection/EstablishmentDetail")

df2 = pd.read_xml("https://ratings.food.gov.uk/api/open-data-files/FHRS501en-GB.xml",
                xpath="/FHRSEstablishment/EstablishmentCollection/EstablishmentDetail/Geocode")

df1 = df1[["BusinessName","BusinessType","PostCode","RatingValue","RatingKey","RatingDate","LocalAuthorityName"]]

pd.set_option('display.max_columns', None)

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

print(df)