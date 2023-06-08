import pandas as pd
import json

# Load the original Excel data
df = pd.read_excel("data/intermediate/single_table/combined_data_sv.xlsx")

# Construct the key based on the location and county
df["key"] = df["location"] + "-" + df["county_sv"]

# Load the geocoded data
with open("data/intermediate/geocoded_locations/cache_geocoded.json", "r", encoding="utf-8") as f:
    geocoded_data = json.load(f)

# Convert the geocoded data into a dictionary for easier lookup
geocoded_dict = {item["original_key"]: item for item in geocoded_data}

# Define a function to match the keys and retrieve the coordinates
def get_coordinates(row):
    key = row["key"]
    if key in geocoded_dict:
        return geocoded_dict[key]["location"]["lat"], geocoded_dict[key]["location"]["lng"]
    else:
        return None, None

# Apply the function to each row in the DataFrame
df[["latitude", "longitude"]] = df.apply(get_coordinates, axis=1, result_type="expand")

# drop key
df.drop("key", axis=1, inplace=True)

# Save the DataFrame as a new Excel file
df.to_excel("data/intermediate/single_table/combined_data_geocoded.xlsx", index=False)
