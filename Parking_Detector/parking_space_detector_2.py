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

    x_left = max(x1, x2)
    y_top = max(y1, y2)
    x_right = min(x1 + w1, x2 + w2)
    y_bottom = min(y1 + h1, y2 + h2)

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    inter_area = (x_right - x_left) * (y_bottom - y_top)
    box1_area = w1 * h1
    box2_area = w2 * h2

    iou = inter_area / float(box1_area + box2_area - inter_area)
    return iou

def non_max_suppression(boxes, threshold=0.4):
    if len(boxes) == 0:
        return []

    boxes = sorted(boxes, key=lambda x: x[2] * x[3], reverse=True)

    selected_boxes = []
    while boxes:
        current_box = boxes.pop(0)
        selected_boxes.append(current_box)
        boxes = [box for box in boxes if compute_iou(current_box, box) < threshold]

    return selected_boxes

def auto_detect_parking_spots(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 1)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 3)
    kernel = np.ones((3, 3), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    edges = cv2.Canny(morph, 30, 120)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    box_sizes = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        x, y, w, h = cv2.boundingRect(approx)
        if 60 < w < 200 and 20 < h < 100:
            box_sizes.append((x, y, w, h))
    
    if box_sizes:
        median_w, median_h = np.median([b[2:] for b in box_sizes], axis=0).astype(int)
    else:
        median_w, median_h = 67, 26

    detected_pos = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        x, y, w, h = cv2.boundingRect(approx)
        if 60 < w < 200 and 20 < h < 100:
            x = x + w // 2 - median_w // 2
            y = y + h // 2 - median_h // 2
            detected_pos.append((x, y, median_w, median_h))

    detected_pos = non_max_suppression(detected_pos, threshold=0.4)

    return detected_pos

# Updated function to handle entries with less than 4 values
def draw_parking_spots(img, posList):
    for pos in posList:
        if len(pos) == 4:
            x, y, w, h = pos
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
        else:
            print(f"Skipping position with incorrect format: {pos}")

def mouseClick(events, x, y, flags, params):
    global posList
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y, 67, 26))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            if len(pos) == 4:
                x1, y1, w, h = pos
                if x1 < x < x1 + w and y1 < y < y1 + h:
                    posList.pop(i)
                    break

    with open('CarParkPos4', 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread(r'D:\Development\parking-management-system-using-CV\Parking Detector\Car Parking.png')
    
    if img is None:
        print("Error: Image not found or unable to load.")
        break
    
    draw_parking_spots(img, posList)
    cv2.putText(img, "Press 'd' to detect spots, 'q' to quit.", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break
    elif key == ord('d'):
        posList = auto_detect_parking_spots(img)
        with open('CarParkPos4', 'wb') as f:
            pickle.dump(posList, f)

cv2.destroyAllWindows()
