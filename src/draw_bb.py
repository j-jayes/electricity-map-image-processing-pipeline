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

# Get the pages for "Blekinge.pdf"
pdf_file = "Blekinge.pdf"
pages_to_convert = table_pages[pdf_file]

# Normalize the filename to ensure special characters are correctly interpreted
normalized_file = unicodedata.normalize('NFC', pdf_file)
# Remove Swedish special characters from the file name
translated_file = normalized_file.translate(str.maketrans(swedish_to_ascii))

for page in pages_to_convert:
    image_path = f"data/intermediate/removed_gray/{translated_file}/{translated_file}_page_{page}.jpg"

    # Read the image
    img = cv2.imread(image_path)

    # Crop 50 pixels from top, bottom and the respective sides based on page number
    img = img[50:-50, 50:-50] if page % 2 != 0 else img[50:-50, :-50]

    # convert the image to grayscale and binarize it
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

    # detect horizontal and vertical lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (100,1))
    detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,100))
    detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

    # Combine the horizontal and vertical detections
    combined = cv2.addWeighted(detect_horizontal, 0.5, detect_vertical, 0.5, 0.0)
    combined = cv2.dilate(combined, None, iterations=2)

    # Find contours in the combined image
    contours, hierarchy = cv2.findContours(combined, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Get the area of the image
    img_area = img.shape[0] * img.shape[1]

    for contour in contours:
        # Get the rectangle around the contour
        x, y, w, h = cv2.boundingRect(contour)
        # Ensure the contour is sufficiently large
        if w * h > img_area / 4 and y > img.shape[0]*0.1:  # Excluding top 10% of the image to avoid page number
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Save the result to the intermediate directory
    os.makedirs(f'data/intermediate/bounding_boxes/{translated_file}', exist_ok=True)
    cv2.imwrite(f'data/intermediate/bounding_boxes/{translated_file}/{translated_file}_page_{page}_table.jpg', img)
