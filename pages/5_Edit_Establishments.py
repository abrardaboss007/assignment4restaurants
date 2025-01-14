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

st.write("Edit establishment")

# Create a searchbox to search different establishments
establishments = df["BusinessName"].tolist()

def search_establishments(searchterm: str):
    # Filter establishments based on the searchterm
    if searchterm:
        return [name for name in establishments if searchterm.lower() in name.lower()]
    return []

london_boroughs = df["LocalAuthorityName"].unique().tolist()

# Use the search function with st_searchbox
selected_value = st_searchbox(
    search_establishments,
    placeholder="Search establishment to edit...",
    key="searchbox_edit",
)

# Display the selected value
if selected_value:
    # Find the index of the selected establishment
    selected_value_index = df.index[df['BusinessName'] == selected_value].tolist()[0]
    
    # Get the current data of the selected establishment
    selected_establishment = df.iloc[selected_value_index]
    
    selected_establishment_image_path = os.path.join("images", "test", f"{selected_establishment['RatingKey']}.png")
    
    with st.container():
        st.write(f"**Establishment name:** {selected_value}")
        st.image(selected_establishment_image_path, width=212)
        
        edit_button = st.button("Edit")
        
        if edit_button:
            # Pre-fill the form fields with the current data
            with st.form(key="Edit", clear_on_submit=True, enter_to_submit=False):
                establishment_name = st.text_input("Establishment Name*", value=selected_establishment["BusinessName"])
                establishment_type = st.selectbox("Establishment Type*", options=["Restaurant/Cafe/Canteen", "Takeaway/sandwich shop"], index=["Restaurant/Cafe/Canteen", "Takeaway/sandwich shop"].index(selected_establishment["BusinessType"]))
                establishment_postcode = st.text_input("Postcode (e.g. E12 5AD)*", value=selected_establishment["PostCode"])
                establishment_rating = st.slider("Hygiene Rating*", min_value=0, max_value=5, step=1, value=selected_establishment["RatingValue"])
                establishment_ratingKey = f"fhrs_{establishment_rating}_en-GB"
                establishment_ratingDate = st.date_input("Rating Date*", value=pd.to_datetime(selected_establishment["RatingDate"]))
                establishment_borough = st.selectbox("Borough Name*", options=london_boroughs, index=london_boroughs.index(selected_establishment["LocalAuthorityName"]))
                longitude = st.text_input("Longitude*", value=selected_establishment["Longitude"])
                latitude = st.text_input("Latitude*", value=selected_establishment["Latitude"])
                
                # Image path (this can remain the same, or you can allow the user to upload a new image)
                image_path = os.path.join("images", "test", f"{establishment_ratingKey}.png")
                
                submit_button = st.form_submit_button(label="Update establishment")
                
                if submit_button:
                    # Validate if any fields are empty
                    if not establishment_name or not establishment_type or not establishment_postcode or not establishment_rating or not establishment_ratingDate or not establishment_borough or not longitude or not latitude:
                        st.warning("Please fill in all mandatory fields")
                    else:
                        # Update the selected row in the DataFrame
                        df.at[selected_value_index, "BusinessName"] = establishment_name
                        df.at[selected_value_index, "BusinessType"] = establishment_type
                        df.at[selected_value_index, "PostCode"] = establishment_postcode
                        df.at[selected_value_index, "RatingValue"] = int(establishment_rating)
                        df.at[selected_value_index, "RatingKey"] = establishment_ratingKey
                        df.at[selected_value_index, "RatingDate"] = establishment_ratingDate.strftime("%Y-%m-%d")
                        df.at[selected_value_index, "LocalAuthorityName"] = establishment_borough
                        df.at[selected_value_index, "Longitude"] = longitude
                        df.at[selected_value_index, "Latitude"] = latitude
                        df.at[selected_value_index, "ImagePath"] = image_path

                        # Save the updated DataFrame to CSV
                        df.to_csv("restaurant_data.csv", index=False)
                        
                        st.success(f"Establishment '{selected_value}' has been updated.")
