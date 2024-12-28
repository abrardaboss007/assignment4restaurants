import pandas as pd

# Function to read the DataFrame from a CSV file
def read_from_csv(filename="restaurant_data.csv"):
    df = pd.read_csv(filename)
    print(f"Data loaded from {filename}")
    return df

# Read the DataFrame back from the CSV
df_loaded = read_from_csv("restaurant_data.csv")

# Check the data
print(df_loaded)