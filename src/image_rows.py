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
    table = gray[y:y+h, x:x+w] # gray table is used for processing

    # Threshold the table image (black = text, white = background)
    _, threshed_table = cv2.threshold(table, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Compute horizontal projection (sum of pixels in each row)
    h_proj = np.sum(threshed_table, axis=1)

    # Compute moving average of horizontal projection
    window_size = 10  # Or another appropriate size
    h_proj_avg = np.convolve(h_proj, np.ones(window_size)/window_size, mode='same')

    # Find row boundaries based on moving average exceeding a threshold
    threshold = np.max(h_proj_avg) / 2  # Or another appropriate threshold
    row_boundaries = np.where(h_proj_avg > threshold)[0]

    # Segment and save each row as a separate image
    for i in range(len(row_boundaries) - 1):
        row_start = row_boundaries[i]
        row_end = row_boundaries[i+1]
        row_img = table[row_start:row_end, :]
        cv2.imwrite(f'data/intermediate/row_images/{image_file}_min_size_{min_size}_row_{i}.jpg', row_img)
