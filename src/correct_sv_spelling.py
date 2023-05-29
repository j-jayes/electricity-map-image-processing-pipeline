# read in combined_data.xlsx from "data/intermediate/single_table"
df = pd.read_excel("data/intermediate/single_table/combined_data.xlsx")

mapping = {
    'Alvsborg': 'Älvsborg',
    'Gavleborg': 'Gävleborg',
    'Goteborgs_och_Bohus': 'Göteborgs och Bohus',
    'Koppaberg': 'Kopparberg',
    'Kristianstad': 'Kristianstad',
    'Kronobergs': 'Kronoberg',
    'Norrbottens_Lan': 'Norrbottens',
    'Orebro': 'Örebro',
    'Ostergotland': 'Östergötland',
    'Skaraborgs_Lan': 'Skaraborgs',
    'Sodermanland': 'Södermanland',
    'Varmland': 'Värmland',
    'Vasterbotten': 'Västerbotten',
    'Vasternorrland': 'Västernorrland',
    'Vastmanland': 'Västmanland'
}

# add a column called "county_sv" to the DataFrame
df["county_sv"] = None
# replace the county names in the "county_sv" column with the Swedish names
df["county_sv"] = df["county"].replace(mapping)

# save data to "data/intermediate/single_table"
df.to_excel("data/intermediate/single_table/combined_data_sv.xlsx", index=False, encoding='utf-8')