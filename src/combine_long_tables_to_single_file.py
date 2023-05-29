import yaml
import pandas as pd
import os

# Load the column indexes from the YAML file
with open("data/intermediate/table_cols.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

# Create a new DataFrame to hold the combined data
combined_df = pd.DataFrame()

# Iterate over the county configurations in the YAML file
for county_cfg in cfg["counties"]:
    county = county_cfg["county"]
    filename = f"{county}_table_long_combined.xlsx"
    filepath = f"data/intermediate/tables_combined_long/{filename}"

    # Load the data from the Excel file
    df = pd.read_excel(filepath)

    # Select the important columns based on the indexes from the YAML file
    # Subtract 1 from each index and select the important columns
    important_columns = df.iloc[:, [county_cfg["user"] - 1, county_cfg["name"] - 1, county_cfg["location"] - 1, county_cfg["source"] - 1, county_cfg["amount"] - 1]]


    # Rename the columns
    important_columns.columns = ["user", "name", "location", "source", "amount"]

    # Add a new column for the county
    important_columns["county"] = county

    # Append the important columns to the combined DataFrame
    combined_df = pd.concat([combined_df, important_columns], ignore_index=True)

# Save the combined DataFrame to a new Excel file
# make folder data/intermediate/single_table
os.makedirs("data/intermediate/single_table", exist_ok=True)
combined_df.to_excel("data/intermediate/single_table/combined_data.xlsx", index=False)
