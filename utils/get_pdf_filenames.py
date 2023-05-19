import os
import json

pdf_folder = "data/input/pdfs/"
output_file = "output.json"

pdf_files = os.listdir(pdf_folder)

pdf_data = {}
for file_name in pdf_files:
    if file_name.endswith(".pdf"):
        pdf_data[file_name] = []

with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(pdf_data, json_file, indent=4, ensure_ascii=False)

print(f"JSON file '{output_file}' created successfully.")
