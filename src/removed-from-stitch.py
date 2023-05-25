
# Specify the stitched images
stitched_files = [f'{file_base}{pair[0]}_{pair[1]}.jpg' for pair in pairs]

# Load the pre-trained text detection model
net = cv2.dnn.readNet("data/models/DB_IC15_resnet50.onnx")

# Specify the output layers
layerNames = [
    "onnx_node!Squeeze_366",
    "onnx_node!Squeeze_367"]


# Specify the input height and width
inputHeight = 736
inputWidth = 1280

for stitched_file in stitched_files:
    # Load the stitched image
    img = cv2.imread(f'data/intermediate/stitched_images/{stitched_file}')

    # Convert the image to a blob and perform a forward pass
    blob = cv2.dnn.blobFromImage(img, 1.0, (inputWidth, inputHeight), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)

    # Process the detections
    rects = []
    confidences = []
    for i in range(0, scores.shape[1]):
        for j in range(0, scores.shape[2]):
            if scores[0, i, j] < 0.5:
                continue
            offsetX = j * 4.0
            offsetY = i * 4.0
            angle = geometry[i, j]
            cos = np.cos(angle)
            sin = np.sin(angle)
            h = scores[0, i, j] + geometry[i, j]
            w = scores[0, i, j] + geometry[i, j]
            endX = int(offsetX + (cos * scores[0, i, j]) + (sin * scores[0, i, j]))
            endY = int(offsetY - (sin * scores[0, i, j]) + (cos * scores[0, i, j]))
            startX = int(endX - w)
            startY = int(endY - h)
            rects.append((startX, startY, endX, endY))
            confidences.append(scores[0, i, j])

    # Calculate the y-coordinate of each row
    rows = sorted([int((rect[1] + rect[3]) / 2) for rect in rects])

    # Draw the lines
    for i in range(1, len(rows)):
        cv2.line(img, (0, rows[i]), (img.shape[1], rows[i]), (0, 0, 0), 2)

    # Save the image
    cv2.imwrite(f'data/intermediate/segmented_images/{stitched_file}', img)
