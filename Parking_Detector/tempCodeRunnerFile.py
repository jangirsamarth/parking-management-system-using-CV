import pickle
import cv2
import numpy as np

# Load existing parking positions if available
try:
    with open('CarParkPos4', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def compute_iou(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    # Compute the coordinates of the intersection rectangle
    x_left = max(x1, x2)
    y_top = max(y1, y2)
    x_right = min(x1 + w1, x2 + w2)
    y_bottom = min(y1 + h1, y2 + h2)

    # Compute the area of intersection rectangle
    if x_right < x_left or y_bottom < y_top:
        return 0.0

    inter_area = (x_right - x_left) * (y_bottom - y_top)

    # Compute the area of both rectangles
    box1_area = w1 * h1
    box2_area = w2 * h2

    # Compute the IoU
    iou = inter_area / float(box1_area + box2_area - inter_area)
    return iou

def non_max_suppression(boxes, threshold=0.4):
    if len(boxes) == 0:
        return []

    boxes = sorted(boxes, key=lambda x: x[2] * x[3], reverse=True)  # Sort by area of box

    selected_boxes = []
    while boxes:
        current_box = boxes.pop(0)
        selected_boxes.append(current_box)
        boxes = [box for box in boxes if compute_iou(current_box, box) < threshold]

    return selected_boxes

# Improved parking spot detection with consistent box size and enhanced accuracy
def auto_detect_parking_spots(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 1)  # Slightly reduce blur kernel size for sharper edges
    
    # Use a more refined adaptive thresholding
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 3)
    
    # Morphological operations to remove noise and close gaps
    kernel = np.ones((3, 3), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # More precise edge detection
    edges = cv2.Canny(morph, 30, 120)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the median size of detected boxes
    box_sizes = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        x, y, w, h = cv2.boundingRect(approx)
        if 60 < w < 200 and 20 < h < 100:  # Filter based on reasonable parking spot sizes
            box_sizes.append((x, y, w, h))
    
    if box_sizes:
        median_w, median_h = np.median([b[2:] for b in box_sizes], axis=0).astype(int)
    else:
        median_w, median_h = 67, 26  # Fallback to default size if no boxes are detected

    detected_pos = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        x, y, w, h = cv2.boundingRect(approx)
        if 60 < w < 200 and 20 < h < 100:  # Filter based on reasonable parking spot sizes
            # Adjust position to align with the white parking lines
            x = x + w // 2 - median_w // 2
            y = y + h // 2 - median_h // 2
            detected_pos.append((x, y, median_w, median_h))

    # Apply non-maximum suppression
    detected_pos = non_max_suppression(detected_pos, threshold=0.4)

    return detected_pos

# Function to draw parking spots on the image
def draw_parking_spots(img, posList):
    for pos in posList:
        x, y, w, h = pos
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)

# Mouse event callback to manually add or remove parking spots
def mouseClick(events, x, y, flags, params):
    global posList
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y, 67, 26))  # Default size for manually added spots
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1, w, h = pos
            if x1 < x < x1 + w and y1 < y < y1 + h:
                posList.pop(i)
                break

    with open('CarParkPos4', 'wb') as f:
        pickle.dump(posList, f)

# Main loop to display the image and handle user interaction
while True:
    img = cv2.imread(r'D:\Development\parking-management-system-using-CV\Parking Detector\Car Parking.png')
    
    if img is None:
        print("Error: Image not found or unable to load.")
        break
    
    # Draw the existing parking spots
    draw_parking_spots(img, posList)

    # Add overlay message
    cv2.putText(img, "Press 'd' to detect spots, 'q' to quit.", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the image with parking spots
    cv2.imshow("Image", img)

    # Enable manual add/remove functionality using mouse clicks
    cv2.setMouseCallback("Image", mouseClick)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break
    elif key == ord('d'):  # Detect parking spots when 'd' is pressed
        posList = auto_detect_parking_spots(img)  # Replace the current list with detected positions
        with open('CarParkPos4', 'wb') as f:
            pickle.dump(posList, f)

cv2.destroyAllWindows()
