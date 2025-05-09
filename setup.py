import os

from data import download_datasets

# create a user folder if it does not exist
def create_folders():
    """
    Create a user folder if it does not exist.
    """
    # Check if the folder exists
    if not os.path.exists('./user'):
        # Create the folder
        os.makedirs('./user', exist_ok=True)
    # Print the path of the user folder
    print("User folder created at: ./user")

def main():
    """
    Main function to create the user folder.
    """
    # Create the user folder
    # Print the process
    print("Creating user folder...")
    create_folders()

    # Download the dataset
    print("Downloading datasets...")
    download_datasets.main()


if __name__ == "__main__":
    main()