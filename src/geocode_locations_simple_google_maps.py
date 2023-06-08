import yaml
import json
import requests
import time
import os

# Load the API key from the config file
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)
API_KEY = config["google_maps"]["key"]

# Load the place names from the JSON file
with open("data/intermediate/geocoded_locations/cache.json", "r", encoding="utf-8") as f:
    places = json.load(f)

# Prepare the base URL for the Google Maps Geocoding API
base_url = "https://maps.googleapis.com/maps/api/geocode/json"

# If the file with geocoded data already exists, load it; otherwise create an empty list
geocoded_file = "data/intermediate/geocoded_locations/cache_geocoded.json"
if os.path.isfile(geocoded_file):
    with open(geocoded_file, "r", encoding="utf-8") as f:
        geocoded_data = json.load(f)
else:
    geocoded_data = []

# Set a counter for the number of processed places
processed_places = len(geocoded_data)

# Iterate over all places, starting from where we left off
for key, value in list(places.items())[processed_places:]:
    try:
        # Extract the county from the key
        county = key.split("-")[-1]

        # Construct the query
        query = f"{value}, {county}, Sweden"

        # Prepare the parameters for the API request
        params = {
            "address": query,
            "key": API_KEY
        }

        # Make the API request
        response = requests.get(base_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the geocoding data
            data = response.json()

            # Check if data was returned
            if data["results"]:
                # Extract the location data
                location_data = data["results"][0]["geometry"]["location"]

                print(f"\nGeocoded {query} to {location_data}")

                # Store the original key, place name, and location data
                geocoded_data.append({
                    "original_key": key,
                    "place": query,
                    "location": location_data
                })
            else:
                print(f"No results for {query}")
        else:
            print(f"API request failed with status code {response.status_code}")

        # Increment the counter of processed places
        processed_places += 1

        # If 100 places have been processed, save the data and sleep for a bit to avoid rate limits
        if processed_places % 100 == 0:
            with open(geocoded_file, "w", encoding="utf-8") as f:
                json.dump(geocoded_data, f, ensure_ascii=False)
            print(f"Processed {processed_places} places, sleeping for a bit...")
            time.sleep(10)  # Adjust the sleep duration as needed
    except Exception as e:
        print(f"An error occurred: {e}")
        continue

# Save the geocoded data to the file one last time at the end
with open(geocoded_file, "w", encoding="utf-8") as f:
    json.dump(geocoded_data, f, ensure_ascii=False)
