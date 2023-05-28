import os
import cv2
import numpy as np
import shutil
from PIL import Image

# Define the base folder path
base_folder = "data/intermediate/removed_gray"

# Iterate over all subfolders in base_folder
for subfolder in os.listdir(base_folder):

    # Get list of all files in the subfolder
    files = sorted(os.listdir(os.path.join(base_folder, subfolder)))

    # Pair up the files (assuming an even number of files)
    pairs = [(files[i], files[i+1]) for i in range(0, len(files), 2)] if len(files) > 1 else [(files[0],)]

    # Iterate over pairs of files
    for pair in pairs:
        # Ensure the destination subfolder exists
        os.makedirs(f'data/intermediate/stitched_images/{subfolder}', exist_ok=True)
        
        if len(pair) == 1:  # If there is only one file, move it to the stitched_images folder
            shutil.copy(os.path.join(base_folder, subfolder, pair[0]), f'data/intermediate/stitched_images/{subfolder}/{pair[0]}')
        else:
            # Form the file paths
            left_file = os.path.join(base_folder, subfolder, pair[0])
            right_file = os.path.join(base_folder, subfolder, pair[1])

            # Open the images
            left_img = Image.open(left_file)
            right_img = Image.open(right_file)

            # Resize the shorter image to the height of the taller one
            max_height = max(left_img.height, right_img.height)
            if left_img.height < max_height:
                left_img = left_img.resize((left_img.width, max_height))
            else:
                right_img = right_img.resize((right_img.width, max_height))

            # Stitch the images together
            stitched_img = Image.fromarray(np.hstack([np.array(left_img), np.array(right_img)]))

            # Save the stitched image
            stitched_img.save(f'data/intermediate/stitched_images/{subfolder}/{pair[0]}_{pair[1]}.jpg')
