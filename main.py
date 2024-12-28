# import pandas as pd, streamlit as st

# # Function to read the DataFrame from a CSV file
# def read_from_csv(filename="restaurant_data.csv"):
#     df = pd.read_csv(filename)
#     print(f"Data loaded from {filename}")
#     return df

# # Read the DataFrame back from the CSV
# df_loaded = read_from_csv("restaurant_data.csv")

# # Check the data
# # print(df_loaded)

# st.write(df_loaded)
# st.image

import pandas as pd
import streamlit as st

# Function to read the DataFrame from a CSV file
def read_from_csv(filename="restaurant_data.csv"):
    df = pd.read_csv(filename)
    print(f"Data loaded from {filename}")
    return df

# Read the DataFrame back from the CSV
df_loaded = read_from_csv("restaurant_data.csv")

# Generate the full path for images (assuming images are in "images/small" in the root folder)
image_base_path = "./images/small"  # Local relative path
df_loaded['FullImagePath'] = df_loaded['ImagePath'].apply(lambda x: image_base_path + x.split('/')[-1])

# Streamlit display
for _, row in df_loaded.iterrows():
    st.write(f"**{row['BusinessName']}**")
    st.write(f"Type: {row['BusinessType']}")
    st.write(f"Rating: {row['RatingValue']}")
    # Render SVG using HTML
    svg_path = row['FullImagePath']
    st.markdown(f'<img src="{svg_path}" alt="Rating" style="width:150px;">', unsafe_allow_html=True)

