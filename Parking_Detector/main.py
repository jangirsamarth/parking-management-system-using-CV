import pickle
import cv2
import cvzone
import numpy as np

# Video feed
cap = cv2.VideoCapture("D:\Development\parking-management-system-using-CV\Parking Detector\Car Parking.mp4")

# Load existing parking positions
try:
    with open('CarParkPos4', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

# SIZE OF BOX IN WHICH CAR IS
width, height = 67, 26

def checkParkingSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        x, y, w, h = pos  # Unpacking (x, y, w, h) instead of (x, y)

        imgCrop = imgPro[y:y + h, x:x + w]  # Adjust cropping based on (x, y, w, h)
        count = cv2.countNonZero(imgCrop)

        # SETTING THE THRESHOLD LIMIT FOR BINARY IMAGE
        if count < 400:
            color = (0, 255, 0)
            thickness = 2
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 1

        cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + h - 3), scale=1, thickness=1, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3, thickness=3, offset=20, colorR=(0, 200, 0))

while True:
    success, img = cap.read()
    
    if not success:
        print("Error: Unable to read the video frame or end of video reached.")
        break
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 2)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)
    cv2.waitKey(10)

cap.release()
cv2.destroyAllWindows()
