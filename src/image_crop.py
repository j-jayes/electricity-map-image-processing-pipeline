import cv2
import numpy as np

# Specify the file name base and page numbers
file_base = "Goteborgs och Bohus.pdf_page_"
pages = [15, 16, 17, 18, 19, 20]

for page in pages:
    # Form the image file name
    image_file = file_base + str(page) + ".jpg"

    # Load the image
    img = cv2.imread(f'data/intermediate/images/{image_file}')

    # Crop 50 pixels off of each edge
    img = img[50:-50, 50:-50]

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
    cv2.imwrite(f'data/intermediate/cropped_images/{image_file}', table)
