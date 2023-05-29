import os
import openai
import json
import yaml
import pandas as pd
import re

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

openai.api_key = config["openai"]["key"]

def geocode_location(place, county, geocoded_locations):
    def remove_json_formatting(text):
        pattern = r'```json\n(.*)\n```'
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1) if match else text

    # Check if we have geocoded this location before
    if place in geocoded_locations:
        return geocoded_locations[place]

    try:
        geocode_prompt = f"What place is this in {county} län Sweden? If you can't find the place, return the place that is most likely based on the letters that have been OCRd. ONLY return RFC 8259 compliant JSON with two keys: 'place_name' and 'description' in a codeblock. The place is: {place}"
        geocode_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in Swedish geography."},
                {"role": "user", "content": f"{geocode_prompt}"}
            ]
        )

        content = geocode_response.choices[0].message.content.strip()

        print(content)

        if content:
            content = remove_json_formatting(content)  # Call the function to remove json formatting
            geocode_input = json.loads(content)
            geocoded_locations[place] = geocode_input  # Save in cache
            return geocode_input
        else:
            raise ValueError('Invalid content: {}'.format(content))

    except Exception as e:
        print(f"Error in geocoding location: {e}")
        return None

df = pd.read_excel("data/intermediate/single_table/combined_data_sv.xlsx")
df["geocode_input"] = None

# Load previously geocoded locations from file, or initialize an empty dictionary
geocoded_locations_file = "data/intermediate/geocoded_locations/geocoded_locations.json"
if os.path.exists(geocoded_locations_file):
    with open(geocoded_locations_file, 'r') as f:
        geocoded_locations = json.load(f)
else:
    geocoded_locations = {}

total_locations = min(15, df.shape[0])

for i, row in df.iloc[:total_locations].iterrows():
    location = row['location']
    county = row['county_sv']

    if pd.isnull(location) or location.strip() == '':
        print(f"Skipping row {i+1}/{total_locations} due to empty location")
        continue

    print(f"Processing row {i+1}/{total_locations}")

    geocoded_location = geocode_location(location, county, geocoded_locations)

    if geocoded_location is not None:
        df.loc[i, "geocode_input"] = json.dumps(geocoded_location)
    else:
        print(f"Geocoding failed for row {i+1}/{total_locations}. Location: {location}")

# Save updated geocoded locations to file
with open(geocoded_locations_file, 'w') as f:
    json.dump(geocoded_locations, f, ensure_ascii=False, indent=4)

df.to_pickle("data/intermediate/single_table/geocoded_locations.pkl")

# open geocoded_locations.pkl and run the following code to get the geocoded locations in a format that can be used in the geocoding notebook
df = pd.read_pickle("data/intermediate/single_table/geocoded_locations.pkl")
df["geocode_input"] = df["geocode_input"].apply(lambda x: json.loads(x))
