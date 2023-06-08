import pandas as pd
import re

# Function to extract the largest integer from a string
def extract_max_number(s):
    s = re.sub(r'(\d) (\d{1}00)', r'\1\2', str(s))  # Remove space between numbers only if followed by 'X00'
    numbers = re.findall(r'\d+', s)
    if not numbers:
        return None
    return max(int(num) for num in numbers)




# Load the DataFrame
df = pd.read_excel("data/intermediate/single_table/combined_data_geocoded.xlsx")

# Apply the function to the 'amount' column
df['amount_clean'] = df['amount'].apply(extract_max_number)

# Save the DataFrame back to the Excel file
df.to_excel("data/intermediate/single_table/combined_data_geocoded_clean_amount.xlsx", index=False)
