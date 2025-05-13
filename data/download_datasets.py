"""Download datasets"""

# Download the file
import requests
import os
import zipfile
import shutil
import pandas as pd

def download_file(url, output_path):
    """
    Download a file from a URL and save it to the specified output path.
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"File downloaded: {output_path}")
    else:
        print(f"Failed to download file: {response.status_code}")

# Unzip the file
def unzip_file(zip_path, extract_to):
    """
    Unzip a file to the specified directory.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"File unzipped: {extract_to}")

# Move the unzipped folder to the desired location
def move_folder(src, dest):
    """
    Move a folder to the specified destination.
    """
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.move(src, dest)
    print(f"Folder moved: {dest}")

# Remove the zip file after extraction
def remove_file(file_path):
    """
    Remove a file.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File removed: {file_path}")
    else:
        print(f"File not found: {file_path}")

def update_csv_paths(csv_folder, old_path, new_path, new_csv_folder):
    """
    Update the paths in the CSV files.
    """
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
    csv_paths = {f: os.path.join(csv_folder, f) for f in csv_files}

    for csv_file, csv_path in csv_paths.items():
        df = pd.read_csv(csv_path)
        # add column name to the dataframe
        df.columns = ['image_path', 'mask_path']
        # For each item, replace the old path with the new path
        df['image_path'] = df['image_path'].apply(lambda x: x.replace(old_path, new_path))
        df['mask_path'] = df['mask_path'].apply(lambda x: x.replace(old_path, new_path))
        # remove the last empty row in the csv
        df = df.dropna()
        df.to_csv(os.path.join(new_csv_folder, os.path.basename(csv_path)), index=False, header=False)

# Check if all files exist in the new path
def check_files_exist(csv_folder, remove=False):
    """
    Check if all files exist in the new path.
    """
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
    for csv_file in csv_files:
        df = pd.read_csv(os.path.join(csv_folder, csv_file))
        for col in df.columns:
            for file_path in df[col]:
                if not os.path.exists(file_path.replace("./user/flair_1_toy_dataset/", "./")):
                    print(f"File {file_path} does not exist.")
                    if remove:
                        # remove the row if the file does not exist
                        df = df[df[col] != file_path]
                        df.to_csv(os.path.join(csv_folder, csv_file), index=False)
                    return False
    return True


def update_csvs():
    """
    Update the file paths in the CSV files.
    """
    # Define the old and new paths
    old_path = "../"
    new_path = "./user/flair_1_toy_dataset/"

    # Define the CSV folder
    csv_folder = "./user/flair_1_toy_dataset/CSVs/"
    new_csv_folder = "./user/flair_1_toy_dataset/csv_toy/"

    # Create the new CSV folder if it does not exist
    if not os.path.exists(new_csv_folder):
        os.makedirs(new_csv_folder, exist_ok=True)

    # Update the paths in the CSV files
    update_csv_paths(csv_folder, old_path, new_path, new_csv_folder)
    check_files_exist(new_csv_folder)


# Main function to download, unzip, move, and remove files
def main():
    url = "https://storage.gra.cloud.ovh.net/v1/AUTH_366279ce616242ebb14161b7991a8461/defi-ia/flair_data_1/flair_1_toy_dataset.zip"
    output_path = "./user/flair_1_toy_dataset.zip"

    if os.path.exists(output_path):
        print(f"File already exists: {output_path}")
    else:
        # Download the file
        download_file(url, output_path)

    if os.path.exists("./user/flair_1_toy_dataset"):
        print("Folder already exists: ./user/flair_1_toy_dataset")
    else:
        # Unzip the file
        unzip_file(output_path, "./user/")

    # # Move the unzipped folder to the desired location
    # move_folder("./user/flair_1_toy_dataset", "./")

    # # Remove the zip file after extraction
    # remove_file(output_path)

    # Print where the data is stored
    print("Data is stored in: ./user/flair_1_toy_dataset")

    if os.path.exists("./user/csv_toy/"):
        print("Folder already exists: ./user/csv_toy/")
    else:
        # Update the CSV files
        update_csvs()
        print("CSV files updated, and saved in ./csv_toy/")

if __name__ == "__main__":
    main()
