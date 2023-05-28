import cv2
import os
import json
import unicodedata

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

# Iterate through each file in the table_pages
for pdf_file, pages_to_convert in table_pages.items():
    # Normalize the filename to ensure special characters are correctly interpreted
    normalized_file = unicodedata.normalize('NFC', pdf_file)
    # Remove Swedish special characters from the file name
    translated_file = normalized_file.translate(str.maketrans(swedish_to_ascii))

    for page in pages_to_convert:
        # Form the image file name
        image_file = f"{translated_file}/{translated_file}_page_{page}.jpg"

        # Load the image
        img = cv2.imread(f'data/intermediate/images/{image_file}')

        # Crop the image differently depending on whether this is the first or second page of the table
        if page % 2 == 1:  # If the page is odd, it's the first page of the table
            img = img[50:-50, 50:-5]
        else:  # If the page is even, it's the second page of the table
            img = img[50:-50, 5:-50]

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply a binary threshold to the image
        _, threshold = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

        # Find the contours in the threshold image
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Sort the contours by area in descending order and keep the largest one
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

        # Find the bounding rectangle of the largest contour then use it to crop the image
        x, y, w, h = cv2.boundingRect(contours[0])
        table = img[y:y+h, x:x+w]

        # Save the cropped image
        os.makedirs(f'data/intermediate/cropped_images/{translated_file}', exist_ok=True)
        cv2.imwrite(f'data/intermediate/cropped_images/{image_file}', table)
