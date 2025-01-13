import pandas as pd, streamlit as st, os
# -----------------------------------------------------------------------------------------------------
# Function to read the DataFrame from a CSV file
@st.cache_data
def read_from_csv(filename="restaurant_data.csv"):
    df_loaded = pd.read_csv(filename)
    print(f"Data loaded from {filename}")
    return df_loaded
# Read the DataFrame back from the CSV
df = read_from_csv("restaurant_data.csv")
# -----------------------------------------------------------------------------------------------------
london_boroughs = list(df["LocalAuthorityName"].unique())
st.write("View establishment")
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

# Function to read the DataFrame from a CSV file
# def read_from_csv(filename="restaurant_data.csv"):
#     df = pd.read_csv(filename)
#     print(f"Data loaded from {filename}")
#     return df

# # Read the DataFrame back from the CSV
# df_loaded = read_from_csv("restaurant_data.csv")

# Generate the full path for images (assuming images are in "images/small" in the root folder)
image_base_path = "./images/small"  # Local relative path
df['FullImagePath'] = df['ImagePath'].apply(lambda x: image_base_path + x.split('/')[-1])

# for _, row in df.iterrows():
#     st.write(f"**{row['BusinessName']}**")
#     st.write(f"Type: {row['BusinessType']}")
#     st.write(f"Rating: {row['RatingValue']}")
#     # Render SVG using HTML
#     png_path = row['ImagePath']
#     st.markdown(f'<img src="{png_path}" alt="Rating" style="width:150px;">', unsafe_allow_html=True)


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


import os
import streamlit as st
import pandas as pd

# Simulate a DataFrame for restaurants
# Example: df = pd.DataFrame({...})
# Assuming df has columns 'BusinessName', 'HygieneRating', and 'RatingKey'

# Constants for pagination
rows_per_page = 25  # Number of rows per page
columns_per_page = 4  # Number of columns per page
total_rows = len(df)  # Total number of rows
items_per_page = rows_per_page * columns_per_page  # Items per page (rows * columns)
total_pages = (total_rows // items_per_page) + (1 if total_rows % items_per_page > 0 else 0)  # Calculate total pages

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
columns = st.columns(columns_per_page)  # 4 columns for display

# Iterate through current_data and display in the grid layout
for i, (index, restaurant) in enumerate(current_data.iterrows()):
    col = columns[i % columns_per_page]  # Cycle through columns
    # Assuming 'BusinessName' and 'HygieneRating' are the columns to display
    name = restaurant['BusinessName']
    hygiene_rating = restaurant['RatingValue']
    
    # Image path (make sure RatingKey exists and the path is correct)
    image_path = os.path.join("images/test", f"{restaurant['RatingKey']}.png")
    
    # Display restaurant info in the selected column
    with col:
        # Ensure consistent height for images and text
        st.image(image_path, width=100, use_container_width = True)  # Use fixed width for alignment
        st.write(f"**{name}**", unsafe_allow_html=True)  # Display BusinessName
        st.write(f"Hygiene Rating: {hygiene_rating}")  # Display HygieneRating

