import os
import openai
import json
import yaml
import pandas as pd
import re
from tqdm import tqdm

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

openai.api_key = config["openai"]["key"]

place_name_pattern = re.compile(r'"place_name":\s*"([^"]+)"')

def extract_place_name(json_string):
    match = place_name_pattern.search(json_string)
    return match.group(1) if match else None

# Load cache from file if it exists, else create a new one
cache_file_path = "data/intermediate/geocoded_locations/cache.json"
try:
    with open(cache_file_path, "r") as cache_file:
        cache = json.load(cache_file)
except FileNotFoundError:
    cache = {}

def save_cache():
    try:
        with open(cache_file_path, "w", encoding='utf-8') as cache_file:
            json.dump(cache, cache_file, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving cache: {e}")

def save_dataframe(df):
    try:
        df.to_pickle("data/intermediate/single_table/geocoded_locations.pkl")
    except Exception as e:
        print(f"Error saving DataFrame: {e}")

def geocode_location(row):
    place, county, name = row['location'], row['county_sv'], row['name']

    if pd.isnull(place) or place.strip() == '':
        place = name
    
    # Check if we already have the result in cache
    cache_key = f"{place}-{county}"
    if cache_key in cache:
        return cache[cache_key]

    try:
        geocode_prompt = f"What place is this in {county} län Sweden? If you can't find the place, return the place that is most likely based on the letters that have been OCRd, knowing that it relates to electricity provision. ONLY return RFC 8259 compliant JSON with two keys: 'place_name' and 'description' in a codeblock. The place is: {place}"
        geocode_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in Swedish geography."},
                {"role": "user", "content": f"{geocode_prompt}"}
            ]
        )

        content = geocode_response.choices[0].message.content.strip()
        place_name = extract_place_name(content)
        cache[cache_key] = place_name  # Store the result in cache
        print(f"\nGeocoded {place} to {place_name}")
        return place_name
    except Exception as e:
        print(f"Error in geocoding location: {e}")
        return None

df = pd.read_excel("data/intermediate/single_table/combined_data_sv.xlsx")


# Apply geocode_location to each row and save after each N rows
N = 10
for i, row in tqdm(df.iterrows(), total=df.shape[0]):
    df.loc[i, "geocode_input"] = geocode_location(row)
    if i % N == 0:
        save_dataframe(df)
        save_cache()

# Save the cache and DataFrame one last time in case total number of rows is not a multiple of N
save_dataframe(df)
save_cache()
