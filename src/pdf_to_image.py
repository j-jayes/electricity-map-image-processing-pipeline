import os
import json
from pdf2image import convert_from_path
import unicodedata

# Load the table pages index
with open('data/input/pdfs/table_pages.json', 'r', encoding='utf-8') as f:
    table_pages = json.load(f)

# Define the translation dictionary
swedish_to_ascii = {
    'Å': 'A',
    'Ä': 'A',
    'Ö': 'O',
    'å': 'a',
    'ä': 'a',
    'ö': 'o',
}

# Iterate through each file in the table_pages
for pdf_file, pages_to_convert in table_pages.items():
    # Normalize the filename to ensure special characters are correctly interpreted
    normalized_file = unicodedata.normalize('NFC', pdf_file)
    # Remove Swedish special characters from the file name
    translated_file = normalized_file.translate(str.maketrans(swedish_to_ascii))

    # Rename the pdf file and convert the relevant pages into images
    os.rename(f'data/input/pdfs/{normalized_file}', f'data/input/pdfs/{translated_file}')
    images = convert_from_path(f'data/input/pdfs/{translated_file}', first_page=pages_to_convert[0], last_page=pages_to_convert[-1])

    # Save the images to the intermediate directory
    os.makedirs(f'data/intermediate/images/{translated_file}', exist_ok=True)
    for i, img in enumerate(images, start=pages_to_convert[0]):
        img.save(f'data/intermediate/images/{translated_file}/{translated_file}_page_{i}.jpg', 'JPEG')

# Rename the keys in table_pages.json file
translated_table_pages = {key.translate(str.maketrans(swedish_to_ascii)): value for key, value in table_pages.items()}

# Save the modified table_pages back to the JSON file
with open('data/input/pdfs/table_pages.json', 'w', encoding='utf-8') as f:
    json.dump(translated_table_pages, f, ensure_ascii=False)
