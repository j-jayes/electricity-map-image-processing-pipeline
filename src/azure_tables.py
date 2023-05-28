import os
import re
import csv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import yaml
import json

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

endpoint = config["azure_access_key"]["endpoint"]
key = config["azure_access_key"]["key"]

def analyze_layout(image_path, json_filename):
    # Check if the result has been computed and saved before
    if os.path.exists(json_filename):
        with open(json_filename, "r") as json_file:
            result_dict = json.load(json_file)
    else:
        document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

        with open(image_path, "rb") as image:
            poller = document_analysis_client.begin_analyze_document("prebuilt-layout", image.read())
            
        result = poller.result()

        result_dict = result.to_dict() # Convert AnalyzeResult object to dict

        # Save the result as a JSON file
        with open(json_filename, "w") as json_file:
            json.dump(result_dict, json_file)

    return result_dict


def export_table_to_csv(table, csv_filename):
    max_row_index = max(cell["row_index"] for cell in table["cells"])
    max_column_index = max(cell["column_index"] for cell in table["cells"])
    rows = [[None for _ in range(max_column_index + 1)] for _ in range(max_row_index + 1)]

    for cell in table["cells"]:
        rows[cell["row_index"]][cell["column_index"]] = cell["content"]

    with open(csv_filename, "w", newline="", encoding='utf-8') as csv_file:  # Add the 'utf-8' encoding here
        writer = csv.writer(csv_file)
        writer.writerows(rows)


def format_filename(filename):
    match = re.search(r"(\w+)\.pdf_page_(\d+)_.*\.jpg", filename)
    if match:
        page = match.group(2)
        return f"page_{page}"
    else:
        return filename

def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


if __name__ == "__main__":
    total_images = sum([len(files) for r, d, files in os.walk("data/intermediate/stitched_images")])
    processed_images = 0

    for root, dirs, files in os.walk("data/intermediate/stitched_images"):
        for filename in files:
            if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")):
                continue

            image_path = os.path.join(root, filename)
            county = os.path.basename(root).replace('.pdf','')
            base_filename = format_filename(filename)
            json_folder = f"data/intermediate/json/{county}"
            ensure_dir_exists(json_folder)
            json_filename = f"{json_folder}/{base_filename}.json"

            result = analyze_layout(image_path, json_filename)

            csv_folder = f"tables_raw/{county}"
            ensure_dir_exists(csv_folder)
            for i, table in enumerate(result["tables"]):
                csv_filename = f"{csv_folder}/{base_filename}_table_{i}.csv"
                export_table_to_csv(table, csv_filename)

            processed_images += 1
            print(f"Processed {processed_images} out of {total_images} images...")