import os
import json
from pdf2image import convert_from_path

# Load the table pages index
with open('data/input/pdfs/table_pages.json', 'r') as f:
    table_pages = json.load(f)

# Specify the PDF file
pdf_file = "Goteborgs och Bohus.pdf"

# Get the relevant page numbers for this PDF
pages_to_convert = table_pages[pdf_file]

# Convert the relevant pages into images
images = convert_from_path(f'data/input/pdfs/{pdf_file}', first_page=pages_to_convert[0], last_page=pages_to_convert[-1])

# Save the images to the intermediate directory
os.makedirs('data/intermediate/images/', exist_ok=True)
for i, img in enumerate(images, start=pages_to_convert[0]):
    img.save(f'data/intermediate/images/{pdf_file}_page_{i}.jpg', 'JPEG')
