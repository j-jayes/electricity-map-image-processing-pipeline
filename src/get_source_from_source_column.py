import pandas as pd

# read dataframe:
df = pd.read_excel("data/intermediate/single_table/combined_data_geocoded_clean_amount.xlsx")

# count items in source column:
df['source'].value_counts()

# save value counts to excel with value and count with filename: data/temp/source_value_counts.xlsx
df['source'].value_counts().to_excel("data/temp/source_value_counts.xlsx")