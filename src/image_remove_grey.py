import cv2
import os
import json
import unicodedata
import numpy as np

# Load the table pages index
with open('data/input/pdfs/table_pages.json', 'r', encoding='utf-8') as f:
    table_pages = json.load(f)

# Define the translation dictionary
swedish_to_ascii = {
    'Å': 'A',
    'Ä': 'A',
    'Ö': 'O',
    'å': 'a',
    'ä': 'a',
    'ö': 'o',
}

# Process all PDFs
for pdf_file in table_pages.keys():
    pages_to_convert = table_pages[pdf_file]

    # Normalize the filename to ensure special characters are correctly interpreted
    normalized_file = unicodedata.normalize('NFC', pdf_file)
    # Remove Swedish special characters from the file name
    translated_file = normalized_file.translate(str.maketrans(swedish_to_ascii))

    # Normalize the filename to ensure special characters are correctly interpreted
    normalized_file = unicodedata.normalize('NFC', pdf_file)
    # Remove Swedish special characters from the file name
    translated_file = normalized_file.translate(str.maketrans(swedish_to_ascii))

    # Define the color range for the gray border
    lower_gray = np.array([0, 0, 120], dtype=np.uint8)
    upper_gray = np.array([0, 0, 125], dtype=np.uint8)

    # Minimum pixel dimensions for cropping
    min_width = 100
    min_height = 100

    # Process each page of Blekinge.pdf
    for page in pages_to_convert:
        # Form the image file name
        image_file = f"{translated_file}/{translated_file}_page_{page}.jpg"

        # Load the image
        img = cv2.imread(f'data/intermediate/images/{image_file}')

        # Convert the image to the HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Create a mask for the gray border
        mask = cv2.inRange(hsv, lower_gray, upper_gray)
        mask = cv2.bitwise_not(mask)

        # Find the contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the bounding rectangle of the largest contour and use it to crop the image
        if contours:
            x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))

            # Check if width and height are above the minimum requirement
            if w > min_width and h > min_height:
                img = img[y:y+h, x:x+w]
            else:
                print(f"Skipping cropping for {image_file} as it is below the minimum size requirement.")

        # Save the image with the bounding box to the intermediate directory
        os.makedirs(f'data/intermediate/removed_gray/{translated_file}', exist_ok=True)
        cv2.imwrite(f'data/intermediate/removed_gray/{image_file}', img)
