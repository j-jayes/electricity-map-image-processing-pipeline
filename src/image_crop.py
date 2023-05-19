import cv2
import numpy as np

# Specify the image file
image_file = "Goteborgs och Bohus.pdf_page_15.jpg"

# Load the image
img = cv2.imread(f'data/intermediate/images/{image_file}')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply smoothing to reduce noise and bleed-through
smoothed = cv2.GaussianBlur(gray, (5, 5), 0)

# Initialize Selective Search
ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
ss.setBaseImage(smoothed)

# Switch to fast but less accurate mode
ss.switchToSelectiveSearchFast()

# Run selective search to get proposed regions
rects = ss.process()

# Iterate over a range of minimum region sizes
for min_size in range(10000, 100000, 10000):  # Adjust the range and step size as needed
    # Filter rects to keep only the ones with sizable area, and sort them by size (largest first)
    filtered_rects = [rect for rect in rects if rect[2]*rect[3] > min_size]
    filtered_rects.sort(key=lambda x: x[2]*x[3], reverse=True)

    # Use the largest region to crop the image
    x, y, w, h = filtered_rects[0]
    table = img[y:y+h, x:x+w]

    # Save the cropped image with the min_size value in the filename
    cv2.imwrite(f'data/intermediate/cropped_images/{image_file}_min_size_{min_size}.jpg', table)
