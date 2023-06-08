import pandas as pd
import json

# Load JSON data
with open('data/intermediate/power_sources/cache.json', 'r', encoding="utf-8") as json_file:
    source_dict = json.load(json_file)

# Load Excel data
df = pd.read_excel('data/intermediate/single_table/combined_data_geocoded_clean_amount.xlsx')

# Check if the 'source' column is present in dataframe
if 'source' in df.columns:
    # Replace source column based on JSON data
    df['source_clean'] = df['source'].map(source_dict).fillna(df['source'])
else:
    print("The 'source' column is not present in the data.")

# Save dataframe back to Excel
df.to_excel('data/intermediate/single_table/combined_data_geocoded_clean_amount_classified_source.xlsx', index=False)
