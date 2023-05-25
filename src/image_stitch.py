import cv2
import numpy as np

from PIL import Image


file_base = "Goteborgs och Bohus.pdf_page_"
pages = [15, 16, 17, 18, 19, 20]

# Pairs of pages to be stitched together
pairs = [(15, 16), (17, 18), (19, 20)]

for pair in pairs:
    # Form the file names
    left_file = f'data/intermediate/cropped_images/{file_base}{pair[0]}.jpg'
    right_file = f'data/intermediate/cropped_images/{file_base}{pair[1]}.jpg'

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
    stitched_img.save(f'data/intermediate/stitched_images/{file_base}{pair[0]}_{pair[1]}.jpg')

