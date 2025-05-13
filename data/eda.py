"""Data exploration"""

# Read the mask image and check the pixel value distribution
import os
import numpy as np
import matplotlib.pyplot as plt
import rasterio
import pandas as pd
from pathlib import Path

# Get the unique pixel values and their counts
def get_pixel_distribution(mask_path):
    with rasterio.open(mask_path) as src:
        mask = src.read(1)
    unique, counts = np.unique(mask, return_counts=True)
    pixel_distribution = pd.DataFrame({'Pixel Value': unique, 'Count': counts, "Mask path": mask_path})
    return pixel_distribution

# Get the pixel value distribution for a list of masks
def get_distribution_for_masks(mask_paths, mask_type=None):
    distributions = pd.DataFrame()
    for mask_path in mask_paths:
        distribution = get_pixel_distribution(mask_path)
        if mask_type is not None:
            distribution['Dataset'] = mask_type
        else:
            distribution['Dataset'] = ''
        distributions = pd.concat([distributions, distribution], ignore_index=True)
    return distributions

# Visualize the pixel value distribution, group by dataset and pixel value
def visualize_pixel_distribution(distributions):
    plt.figure(figsize=(12, 6))

    plt.bar(distributions['Pixel Value'], distributions['Count'], label="Dataset", alpha=0.5)
    plt.xlabel('Pixel Value')
    plt.ylabel('Count')
    plt.title('Pixel Value Distribution')
    plt.legend()
    plt.show()

# Read the mask and image paths from CSV
def read_csv_paths(csv_path):
    df = pd.read_csv(csv_path)
    # add column name to the dataframe
    df.columns = ['image_path', 'mask_path']
    image_paths = df['image_path'].tolist()
    mask_paths = df['mask_path'].tolist()
    return image_paths, mask_paths

# visualize a image and a mask pair
def visualize_image_and_mask(mask_path, image_path=None):
    if image_path is None:
        image_path = str(mask_path).replace('MSK', 'IMG').replace("msk", "img").replace("labels", "aerial")

    # visualize 3 band image
    with rasterio.open(image_path) as src_img:
        image = src_img.read([1, 2, 3]).swapaxes(0, 2).copy()
        image = image / 255.0  # Normalize the image to [0, 1] range

    # visualize mask
    with rasterio.open(mask_path) as src_msk:
        mask = src_msk.read(1).copy()

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].imshow(image)
    ax[0].set_title('Image')
    ax[0].axis('off')

    ax[1].imshow(mask, cmap='gray')
    ax[1].set_title('Mask')
    ax[1].axis('off')

    plt.show()

def main():
    # Read the mask and image paths from CSV
    print("Retrieve the image paths...")
    _, mask_paths_train = read_csv_paths('../user/flair_1_toy_dataset/csv_toy/flair-1-paths-toy-train.csv')
    _, mask_paths_val = read_csv_paths('../user/flair_1_toy_dataset/csv_toy/flair-1-paths-toy-val.csv')
    _, mask_paths_test = read_csv_paths('../user/flair_1_toy_dataset/csv_toy/flair-1-paths-toy-test.csv')
    # update the paths according to the relative path to this script
    mask_paths_train = [Path(__file__).parent.parent / mask_path for mask_path in mask_paths_train]
    mask_paths_val = [Path(__file__).parent.parent / mask_path for mask_path in mask_paths_val]
    mask_paths_test = [Path(__file__).parent.parent / mask_path for mask_path in mask_paths_test]


    # Visualize a pair of image and mask
    print("Visualize a pair of image and mask...")
    visualize_image_and_mask(mask_paths_train[0], image_path=None)

    print("Get the pixel value distribution for train, val, and test masks...")
    # Get the pixel value distribution for the training masks
    distributions_train = get_distribution_for_masks(mask_paths_train, mask_type='Train')
    # Get the pixel value distribution for the validation masks
    distributions_val = get_distribution_for_masks(mask_paths_val, mask_type='Validation')
    # Get the pixel value distribution for the test masks
    distributions_test = get_distribution_for_masks(mask_paths_test, mask_type='Test')
    # Combine all distributions
    all_distributions = pd.concat([distributions_train, distributions_val, distributions_test], ignore_index=True)

    # Group by pixel value and take the sum of the count
    all_distributions = all_distributions.groupby(['Pixel Value', 'Dataset'])['Count'].sum().reset_index()

    print("Visualize the pixel value distribution...")
    # Visualize the pixel value distribution
    visualize_pixel_distribution(all_distributions)


def class_dict():
    class_dict = {
        "building": 1,
        "pervious surface": 2,
        "impervious surface": 3,
        "bare soil": 4,
        "water": 5,
        "coniferous": 6,
        "deciduous": 7,
        "brushwood": 8,
        "vineyard": 9,
        "herbaceous vegetation": 10,
        "agricultural land": 11,
        "plowed land": 12,
        "swimming pool": 13,
        "snow": 14,
        "clear cut": 15,
        "mixed": 16,
        "ligneous": 17,
        "greenhouse": 18,
        "other": 19
    }
    return class_dict


if __name__ == "__main__":
    main()
