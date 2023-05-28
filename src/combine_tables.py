import csv
import json
import os
import re
import pandas as pd

def ensure_dir_exists(dir_path):
    os.makedirs(dir_path, exist_ok=True)

def cells_to_rows(cells):
    max_row_index = max(cell["row_index"] for cell in cells)
    max_column_index = max(cell["column_index"] for cell in cells)

    rows = [[None for _ in range(max_column_index + 1)] for _ in range(max_row_index + 1)]

    for cell in cells:
        rows[cell["row_index"]][cell["column_index"]] = cell["content"]
    
    return rows

def combine_tables_horizontally(tables):
    # Get the unique row indexes and sort them
    unique_row_indexes = sorted(set(cell["row_index"] for table in tables for cell in table["cells"]))

    # Create a list to store the combined rows
    combined_rows = []

    # For each unique row index, create a combined row
    for row_index in unique_row_indexes:
        combined_row = []

        # For each table, get the cells for the current row index and add their content to the combined row
        for table in tables:
            row_cells = [cell for cell in table["cells"] if cell["row_index"] == row_index]

            # If there are no cells for the current row index in this table, add a None value
            if not row_cells:
                combined_row.append(None)
            else:
                # Sort the cells by their column index and add their content to the combined row
                row_cells.sort(key=lambda cell: cell["column_index"])
                combined_row.extend(cell["content"] for cell in row_cells)

        combined_rows.append(combined_row)

    return combined_rows


def combine_and_save_tables(json_filename, excel_filename):
    with open(json_filename, "r") as f:
        result = json.load(f)

    combined_rows = combine_tables_horizontally(result["tables"])

    # Create a pandas DataFrame from combined_rows
    df = pd.DataFrame(combined_rows)

    # Save the DataFrame to an Excel file
    df.to_excel(excel_filename, index=False, encoding='utf-8')

if __name__ == "__main__":
    # Iterate through all JSON files in the specified directory
    for root, dirs, files in os.walk("data/intermediate/json"):
        for filename in files:
            if not filename.lower().endswith(".json"):
                continue

            json_path = os.path.join(root, filename)
            county = os.path.basename(root)
            base_filename = os.path.splitext(filename)[0]
            excel_folder = f"data/intermediate/tables_combined/{county}"
            ensure_dir_exists(excel_folder)
            excel_filename = f"{excel_folder}/{base_filename}_combined.xlsx"

            combine_and_save_tables(json_path, excel_filename)