# # -----------------------------------------------------------------------------------------------------
import pandas as pd
import streamlit as st
import os
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
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
# Filters Class
class Filters:
    def __init__(self, dataframe):
        self.original_df = dataframe
        self.filtered_df = dataframe.copy()
        self.geolocator = Nominatim(user_agent="restaurant_locator")

    def filter_hygiene_rating(self):
        hygiene_rating_input = st.selectbox(
            "Filter by hygiene rating",
            options=["5", "4 or above", "3 or above", "2 or above", "1 or above", "All"], 
            index=5, 
            placeholder="Pick a value"
        )
        if hygiene_rating_input == "5":
            self.filtered_df = self.filtered_df[self.filtered_df["RatingValue"] == 5]
        elif hygiene_rating_input == "4 or above":
            self.filtered_df = self.filtered_df[self.filtered_df["RatingValue"] >= 4]
        elif hygiene_rating_input == "3 or above":
            self.filtered_df = self.filtered_df[self.filtered_df["RatingValue"] >= 3]
        elif hygiene_rating_input == "2 or above":
            self.filtered_df = self.filtered_df[self.filtered_df["RatingValue"] >= 2]
        elif hygiene_rating_input == "1 or above":
            self.filtered_df = self.filtered_df[self.filtered_df["RatingValue"] >= 1]

    def filter_hygiene_update_date(self):
        self.filtered_df['RatingDate'] = pd.to_datetime(self.filtered_df['RatingDate'], errors='coerce')
        hygiene_update_input = st.date_input("Filter by when hygiene rating was last updated", value=None)
        if hygiene_update_input:
            self.filtered_df = self.filtered_df[self.filtered_df["RatingDate"] > pd.Timestamp(hygiene_update_input)]

    def filter_by_radius(self):
        radius_text = st.markdown("**Radius Filter**")
        postcode_input = st.text_input("Enter your postcode:")
        radius_input = st.slider("Select radius (in km):", min_value=0.0, max_value=10.0, value=10.0, step = 0.5)
        if postcode_input:
            try:
                user_location = self.geolocator.geocode(postcode_input)
                if user_location:
                    user_coordinates = (user_location.latitude, user_location.longitude)
                    self.filtered_df['DistanceFromUser'] = self.filtered_df.apply(
                        lambda row: geodesic((row['Latitude'], row['Longitude']), user_coordinates).km, axis=1
                    )
                    self.filtered_df = self.filtered_df[self.filtered_df['DistanceFromUser'] <= radius_input]
                else:
                    st.warning("Could not find the specified postcode.")
            except Exception as e:
                st.error(f"Error in geocoding: {e}")

    def apply_filters(self):
        self.filter_hygiene_rating()
        self.filter_hygiene_update_date()
        self.filter_by_radius()
        return self.filtered_df

# -----------------------------------------------------------------------------------------------------
# Create a searchbox to search different establishments
establishments = df["BusinessName"].tolist()

def search_establishments(searchterm: str):
    if searchterm:
        return [name for name in establishments if searchterm.lower() in name.lower()]
    return []

# Use the search function with st_searchbox
st.markdown("**Type the name of an establishment or carry on scrolling to view all**")
selected_value = st_searchbox(
    search_establishments,
    placeholder="Search establishments...",
    key="searchbox_key",
)

# Display the selected value
if selected_value:
    selected_value_index = df.index.get_loc(df.loc[df['BusinessName'] == f"{selected_value}"].index[0])
    selected_establishment_image_path = os.path.join(r"images\test", f"{df.iloc[selected_value_index]['RatingKey']}.png")
    with st.container(border=True, height=300):
        st.write(f"**Establishment name:** {selected_value}")
        st.image(selected_establishment_image_path, width=212)

# -----------------------------------------------------------------------------------------------------
# Apply Filters
filters = Filters(df)
filtered_df = filters.apply_filters()

# -----------------------------------------------------------------------------------------------------
# Pagination feature for viewing establishments
rows_per_page, columns_per_page = 25, 4
total_rows = len(filtered_df)
items_per_page = rows_per_page * columns_per_page
total_pages = (total_rows // items_per_page) + (1 if total_rows % items_per_page > 0 else 0)

# Sidebar navigation for page number
st.sidebar.title("Pagination")
current_page = st.sidebar.number_input("Page:", min_value=1, max_value=total_pages, value=1)

# Calculate start and end indices for the current page
start_index = (current_page - 1) * items_per_page
end_index = start_index + items_per_page
current_data = filtered_df.iloc[start_index:end_index]

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
    
    with col:
        with st.container(border=True, height=250):
            st.image(image_path, width=100, use_container_width=True)
            st.write(f"**{name}**", unsafe_allow_html=True)
            st.write(f"Hygiene Rating: {hygiene_rating}")

st.write(f"Displaying page {current_page} of {total_pages}")
