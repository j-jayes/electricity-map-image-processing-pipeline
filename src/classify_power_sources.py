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

power_source_pattern = re.compile(r'"power_source":\s*"([^"]+)"')


def extract_power_source(json_string):
    match = power_source_pattern.search(json_string)
    return match.group(1) if match else None


# Load cache from file if it exists, else create a new one
cache_file_path = "data/intermediate/power_sources/cache.json"
try:
    with open(cache_file_path, "r") as cache_file:
        cache = json.load(cache_file)
except FileNotFoundError:
    cache = {}


def save_dataframe(df):
    try:
        df.to_pickle(
            "data/intermediate/power_sources/classified_power_sources.pkl")
    except Exception as e:
        print(f"Error saving DataFrame: {e}")


def save_cache():
    with open(cache_file_path, 'w', encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=4)


def classify_power_source(source_in):
    if pd.isnull(source_in) or source_in.strip() == '':
        return None

    if source_in in cache:
        return cache[source_in]

    try:
        source_prompt = f"""
            - Role: You are a classifier.
            - Data: You're working with OCR data related to power sources at Swedish power stations and electricity plants from the 1920s.
            - The power sources could be:
                - 'Water power' indicated by 'Vatten' or 'v'.
                - 'Steam' indicated by 'Ångturbin' or 'å'.
                - 'Diesel' indicated by 'd'.
                - 'Transmitted' power, usually indicated by 'Ab. från' or a location name like 'Ängelholm'.
            - Misinterpretations: OCR entries that are only punctuation or digits should be classified as 'NULL' (e.g. '0', '1', '>>').
            - Task: Given an instance, classify it as 'water', 'steam', 'diesel', 'transmitted', or 'NULL'.
            - Output: The output should be in RFC 8259 compliant JSON with the key 'power_source'.
            - ONLY return RFC 8259 compliant JSON with the key: 'power_source', no other text. The entry is: {source_in}"""
        source_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                    "content": "You are an expert in Swedish electrification."},
                {"role": "user", "content": f"{source_prompt}"}
            ]
        )

        content = source_response.choices[0].message.content.strip()
        power_source = extract_power_source(content)
        print(f"\nClassified {source_in} as {power_source}")
        cache[source_in] = power_source
        return power_source
    except Exception as e:
        print(f"Error in classifying location: {e}")
        return None


df = pd.read_excel("data/intermediate/power_sources/source_value_counts.xlsx")

# Vectorized approach to classify sources
df["power_source_classified"] = df["source"].apply(classify_power_source)
save_dataframe(df)
save_cache()
