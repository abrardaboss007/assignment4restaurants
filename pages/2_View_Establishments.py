import pandas as pd
import streamlit as st
import os
from streamlit_searchbox import st_searchbox
# -----------------------------------------------------------------------------------------------------
# Function to read the DataFrame from a CSV file
@st.cache_data
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
    placeholder="Search establishments...",
    key="searchbox_key",
)

#Display the selected value
if selected_value:
    selected_value_index = df.index.get_loc(df.loc[df['BusinessName'] == f"{selected_value}"].index[0])
    selected_establishment_image_path = os.path.join(r"images\test", f"{df.iloc[selected_value_index]["RatingKey"]}.png")
    with st.container(border = True, height = 300):
        st.write(f"**Establishment name:** {selected_value}")
        st.image(selected_establishment_image_path, width = 212)
# -----------------------------------------------------------------------------------------------------
# Pagination feature for viewing establishments 

# Constants for pagination
rows_per_page = 25  
columns_per_page = 4  
total_rows = len(df)  
items_per_page = rows_per_page * columns_per_page  
total_pages = (total_rows // items_per_page) + (1 if total_rows % items_per_page > 0 else 0)  

# Sidebar navigation for page number
st.sidebar.title("Pagination")
current_page = st.sidebar.number_input("Page:", min_value=1, max_value=total_pages, value=1)

# Calculate start and end indices for the current page
start_index = (current_page - 1) * items_per_page
end_index = start_index + items_per_page
current_data = df.iloc[start_index:end_index]

# Display page information
st.write(f"Displaying page {current_page} of {total_pages}")

# Create a grid layout to display restaurants
columns = st.columns(columns_per_page) 

# Iterate through current_data and display in the grid layout
for i, (index, restaurant) in enumerate(current_data.iterrows()):
    col = columns[i % columns_per_page]  # Cycle through columns
    name = restaurant['BusinessName']
    hygiene_rating = restaurant['RatingValue']
    image_path = os.path.join(r"images\test", f"{restaurant['RatingKey']}.png")
    
    # Display restaurant info in the selected column
    with col:
        with st.container(border=True, height=250):
            st.image(image_path, width=100, use_container_width = True)  
            st.write(f"**{name}**", unsafe_allow_html=True)  
            st.write(f"Hygiene Rating: {hygiene_rating}")  

st.write(f"Displaying page {current_page} of {total_pages}")
# -----------------------------------------------------------------------------------------------------
# Creating three filters 

# Create filter based on hygiene rating 

# Create filter based on when hygiene rating was last updated

# Create filter based on location and radius of restaurants/establishments


# -----------------------------------------------------------------------------------------------------




# -----------------------------------------------------------------------------------------------------
london_boroughs = list(df["LocalAuthorityName"].unique())
df["RatingValue"] = df["RatingValue"].astype(int)


empty_list = []
for borough in london_boroughs:
    borough_df = df[df["LocalAuthorityName"].isin([borough])]
    mean = borough_df["RatingValue"].mean()
    empty_list.append(mean)
    print(borough_df)


def mean(borough):
    list_1 = []
    borough_df = df[df["LocalAuthorityName"].isin([borough])]
    average = borough_df["RatingValue"].mean()
    return average

i = 0
for borough in london_boroughs:
    print(f"{borough} has an average hygiene rating of {empty_list[i]}")
    i += 1


# for restaurant in range(len(df)):
#     st.write(f"**Name: {df.loc[restaurant,"BusinessName"]}**")
#     st.write(f"Type: {df.loc[restaurant,"BusinessType"]}")
#     st.write(f"Rating: {df.loc[restaurant,"RatingValue"]}")
#     st.image(os.path.join(r"images\test",f"{df.loc[restaurant,"RatingKey"]}.png"), width = 212)

# Pagination variables
# rows_per_page = 25  # Number of rows per page
# total_rows = len(df)
# items_per_page = rows_per_page * 4
# total_pages = (total_rows // items_per_page) + (1 if total_rows % items_per_page > 0 else 0)

# # Sidebar navigation
# st.sidebar.title("Pagination")
# current_page = st.sidebar.number_input("Page:", min_value=1, max_value=total_pages, value=1)

# # Calculate start and end indices for the current page
# start_index = (current_page - 1) * items_per_page
# end_index = start_index + items_per_page
# current_data = df.iloc[start_index:end_index]


# # Display current page data
# st.write(f"Displaying page {current_page} of {total_pages}")
# #st.dataframe(current_data)
# for restaurant in current_data:
#     #st.write(f"**Name: {df.loc[restaurant,"BusinessName"]}**")
#     image = os.path.join(r"images\test",f"{current_data.loc[restaurant,"RatingKey"]}.png")
#     st.image([image], width = 212)

# for restaurant in range(len(df)):
#     st.write(f"**Name: {df.loc[restaurant,"BusinessName"]}**")
#     image = os.path.join(r"images\test",f"{df.loc[restaurant,"RatingKey"]}.png")
#     st.image([image], width = 212)