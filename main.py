import pandas as pd, streamlit as st, os
from api_data import add_image_paths
# Function to read the DataFrame from a CSV file
def read_from_csv(filename="restaurant_data.csv"):
    df_loaded = pd.read_csv(filename)
    print(f"Data loaded from {filename}")
    return df_loaded

# Read the DataFrame back from the CSV
df = read_from_csv("restaurant_data.csv")

# Check the data
#print(df)

london_boroughs = list(df["LocalAuthorityName"].unique())
print(london_boroughs)

df["RatingValue"] = df["RatingValue"].astype(int)
empty_list = []
for borough in london_boroughs:
    borough_df = df[df["LocalAuthorityName"].isin([borough])]
    mean = borough_df["RatingValue"].mean()
    empty_list.append(mean)
    print(borough_df)


i = 0
for borough in london_boroughs:
    print(f"{borough} has an average hygiene rating of {empty_list[i]}")
    i += 1
#st.write(df)

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

for _, row in df.iterrows():
    st.write(f"**{row['BusinessName']}**")
    st.write(f"Type: {row['BusinessType']}")
    st.write(f"Rating: {row['RatingValue']}")
    # Render SVG using HTML
    png_path = row['ImagePath']
    st.markdown(f'<img src="{png_path}" alt="Rating" style="width:150px;">', unsafe_allow_html=True)

edit_button = st.button("Something doesnt look right ? Edit it here", use_container_width=True)
add_button = st.button("Want to add an establishment? Click here", use_container_width=True)
remove_button = st.button("Want to remove a restaurant? Click here", use_container_width=True)

if edit_button:
    print("Fine go on then edit")

if add_button:
    print("Add a restaurantttt")

if remove_button:
    print("You want to remove my restaurants????")
    