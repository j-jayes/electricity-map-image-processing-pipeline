import pandas as pd
import os

def combine_excel_sheets_to_one(excel_folder, combined_long_folder):
    # Collect all the Excel files in the given directory
    filenames = [f for f in os.listdir(excel_folder) if f.endswith('.xlsx')]
    
    dfs = []  # A list to hold all the DataFrames
    
    for filename in filenames:
        filepath = os.path.join(excel_folder, filename)
        
        # Load the data from the Excel file
        df = pd.read_excel(filepath)

        # Check if all DataFrames have the same number of columns
        if dfs and (len(df.columns) != len(dfs[0].columns)):
            print(f"Warning: {filename} does not have the same number of columns")

        dfs.append(df)

    # Concatenate all the DataFrames
    combined_df = pd.concat(dfs, ignore_index=True)

    # Get the name of the subfolder and use it to name the new Excel file
    subfolder_name = os.path.basename(excel_folder)
    combined_long_filename = f"{subfolder_name}_table_long_combined.xlsx"
    combined_long_filepath = os.path.join(combined_long_folder, combined_long_filename)

    # Save the combined DataFrame to a new Excel file
    combined_df.to_excel(combined_long_filepath, index=False)

if __name__ == "__main__":
    # Create the "data/intermediate/tables_combined_long" directory if it doesn't exist
    combined_long_folder = "data/intermediate/tables_combined_long"
    os.makedirs(combined_long_folder, exist_ok=True)

    # Iterate over the subfolders in "data/intermediate/tables_combined"
    combined_tables_dir = "data/intermediate/tables_combined"
    subfolders = [f.path for f in os.scandir(combined_tables_dir) if f.is_dir()]
    
    for subfolder in subfolders:
        combine_excel_sheets_to_one(subfolder, combined_long_folder)
