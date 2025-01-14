import pandas as pd
import streamlit as st
import os
from streamlit_searchbox import st_searchbox
# -----------------------------------------------------------------------------------------------------
# Function to read the DataFrame from a CSV file

def read_from_csv(filename="restaurant_data.csv"):
    df_loaded = pd.read_csv(filename)
    print(f"Data loaded from {filename}")
    return df_loaded

# Read the DataFrame back from the CSV
df = read_from_csv("restaurant_data.csv")

# Generate the full path for images
image_base_path = "./images/small"  # Local relative path
df['FullImagePath'] = df['ImagePath'].apply(lambda x: image_base_path + x.split('/')[-1])
# -----------------------------------------------------------------------------------------------------
# Create a searchbox to search different for london boroughs
london_boroughs = df["LocalAuthorityName"].unique().tolist()

def search_boroughs(searchterm: str):
    # Filter establishments based on the searchterm
    if searchterm:
        return [name for name in london_boroughs if searchterm.lower() in name.lower()]
    return []

st.write("Add establishment")

with st.form(key = "Add", clear_on_submit=True, enter_to_submit=False, border=True,):
    establishment_name = st.text_input(label = "Establishment Name*")
    establishment_type = st.selectbox(label="Establishment Type*", options=["Restaurant/Cafe/Canteen","Takeaway/sandwich shop"])
    establishment_postcode = st.text_input(label= "Postcode (e.g. E12 5AD)*")
    establishment_rating = st.slider(label= "Hygiene Rating*" , min_value=0, max_value=5, step=1)
    establishment_rating = str(establishment_rating)
    establishment_ratingKey = f"fhrs_{establishment_rating}_en-GB"
    establishment_ratingDate = st.date_input(label = "Rating Date*")
    establishment_borough = st.selectbox(label="Borough Name*", options=london_boroughs)
    longitude = st.text_input(label = "Longitude*")
    latitude = st.text_input(label = "Latitude*")
    image_path = os.path.join(r"images/test", f"/{establishment_ratingKey}.png")
    #image_path = 
    submit_button = st.form_submit_button(label="Add establishment")
    if submit_button:
        if not establishment_name or not establishment_type or not establishment_postcode or not establishment_rating or not establishment_ratingDate or not establishment_borough or not longitude or not latitude:
            st.warning("Please fill in all mandatory fields")
            st.stop()
        else:
            new_row = pd.DataFrame(
                [
                    {
                        "BusinessName":establishment_name,
                        "BusinessType":establishment_type,
                        "PostCode":establishment_postcode,
                        "RatingValue":int(establishment_rating),
                        "RatingKey":establishment_ratingKey,
                        "RatingDate":establishment_ratingDate.strftime("%Y-%m-%d"),
                        "LocalAuthorityName":establishment_borough,
                        "Longitude":longitude,
                        "Latitude":latitude,
                        "ImagePath":image_path
                    }
                ]
            )

            updated_df = pd.concat([df,new_row], ignore_index=True)
            updated_df.to_csv("restaurant_data.csv", index=False)
            st.success("Establishment data has been added!")