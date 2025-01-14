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


st.write("Remove establishment")

# Create a searchbox to search different establishments
establishments = df["BusinessName"].tolist()

def search_establishments(searchterm: str):
    # Filter establishments based on the searchterm
    if searchterm:
        return [name for name in establishments if searchterm.lower() in name.lower()]
    return []

# Use the search function with st_searchbox
selected_value = st_searchbox(
    search_establishments,
    placeholder="Search establishment to delete...",
    key="searchbox_delete",
)

#Display the selected value
if selected_value:
    selected_value_index = df.index.get_loc(df.loc[df['BusinessName'] == f"{selected_value}"].index[0])
    selected_establishment_image_path = os.path.join(r"images/test", f"{df.iloc[selected_value_index]["RatingKey"]}.png")
    with st.container(border = True, height = 300):
        st.write(f"**Establishment name:** {selected_value}")
        st.image(selected_establishment_image_path, width = 212)
        delete_button = st.button("Delete")
        if delete_button:
            df = df.drop(selected_value_index)
            df.to_csv("restaurant_data.csv", index=False)
            st.success("Establishment has been removed")