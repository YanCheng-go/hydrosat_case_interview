"""Download datasets"""

# Download the file
import requests
import os
import zipfile
import shutil
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

# Main function to download, unzip, move, and remove files
def main():
    url = "https://storage.gra.cloud.ovh.net/v1/AUTH_366279ce616242ebb14161b7991a8461/defi-ia/flair_data_1/flair_1_toy_dataset.zip"
    output_path = "./user/flair_1_toy_dataset.zip"
    # Download the file
    download_file(url, output_path)

    # Unzip the file
    unzip_file(output_path, "./user/")

    # # Move the unzipped folder to the desired location
    # move_folder("./user/flair_1_toy_dataset", "./")

    # # Remove the zip file after extraction
    # remove_file(output_path)

    # Print where the data is stored
    print("Data is stored in: ./user/flair_1_toy_dataset")

if __name__ == "__main__":
    main()
