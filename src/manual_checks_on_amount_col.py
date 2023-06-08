# I have manually checked the values in the amount column of the table, and fixed them in a column called "amount_manual". Now I combine these back into the tabl

import pandas as pd
import pathlib
import numpy as np


# Load your Excel file
path_in = pathlib.Path.cwd() / "data" / "intermediate" / "single_table" / "combined_data_geocoded_clean_amount_classified_source_manual_edits.xlsx"

df = pd.read_excel(path_in)

# Create the 'amount_final' column
df['amount_final'] = df['amount_manual'].where(df['amount_manual'].notna(), df['amount_clean'])

# Now I want to fix the power source column

# count unique values in the power source column called "source_clean"
# Create a dictionary with the unique values as keys and initialize the values as None
unique_values_dict = {value: None for value in df['source_clean'].unique()}

# Print the dictionary in a format that can be copied into a Python script
unique_values_dict = {
    'nan': None,
    'water': "water",
    'transmitted': "transmitted",
    'd': "diesel",
    'steam': "steam",
    'Diesel':  "diesel",
    'diesel': "diesel",
    'Kraftstationen samt större delen av distributionsnätet beläget i': None,
    'Vatten- turbin Ang- maskin Vatten- turbin': "water",
    'Drivkraft': None,
    '-:unselected:': None,
    '- -': None,
    'water/steam': "water",
    'v. och d.': "water",
    '[2×220': None,
    'Vatten- turbiner Angturbin Råoljemotor': "water",
    '7': None,
    'V å': None,
    'Ab. från citetsverk,': "transmitted",
    'water/steam/transmitted': "water",
    'Malmö Ab. från': "transmitted",
    'Ab. från Andelsföreningen Bjärnums Elektricitetsverk, Bjärnum': "transmitted",
    'Ohs Ab. fr. Sydsvenska Kraft A .- B.': "transmitted",
    'v d 0': "water",
    '3.5 -': None,
    'å v': "steam",
    '10000/lågsp.': None,
    'ånga vatten': "steam",
    'diesel vatten': "diesel",
    'vatten ånga': "water",
    'Kvarnforsen, 2 stationer': "transmitted",
    'Holaforsen': "transmitted",
    'Skalmsjö': "transmitted",
    'Lännäs': "transmitted",
    'Källom': "transmitted",
    'Abon. från Gammelbyns Kraft A .- B.': "transmitted",
    'Norum': "transmitted",
    'Lo kraftstation': "transmitted",
    'Ulvvik': "transmitted",
    'Ofverdal': "transmitted",
    'Furuhult': "transmitted",
    'Vatten': "water",
    'vatten': "water",
    'By': "transmitted",
    'Gröde': "transmitted",
    'Kjäl': "transmitted",
    'Utansjö': "transmitted",
    'Lögdö': "transmitted",
    '/ Vatten Diesel Vatten': "water",
    '5': None
    }


# Create the 'source_final' column
df['source_clean'] = df['source_clean'].map(unique_values_dict)


# Set up the soure_final column


# Create the conditions
conditions = [
    (df['amount_final'].isna()), 
    ((df['amount_final'].notna()) & (df['amount_final'] != 0) & (df['source_clean'].notna())),
    ((df['amount_final'].notna()) & (df['source_clean'].isna()))
]

# Create the choices
choices = ['transmitted', df['source_clean'], 'water']

# Create the new column
df['source_final'] = np.select(conditions, choices, default=np.nan)

# Downward fill the 'source_final' column
df['source_final'] = df['source_final'].fillna(method='ffill')

# Downward fill the 'latitude' and 'longitude' column
df['latitude'] = df['latitude'].fillna(method='ffill')
df['longitude'] = df['longitude'].fillna(method='ffill')

# save the file
path_out = pathlib.Path.cwd() / "data" / "intermediate" / "single_table" / "combined_data_manual_edits_source_amount.xlsx"

# save the file with the path_out
df.to_excel(path_out, index=False)
