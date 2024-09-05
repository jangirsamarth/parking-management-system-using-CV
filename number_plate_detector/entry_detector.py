import time
import cv2
import imutils
import mysql.connector
import numpy as np
import pytesseract
import re
from datetime import datetime

# Initialize logging
import logging
logging.basicConfig(level=logging.INFO)

# Using SQL for database management
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="spms"
    )
    mycursor = mydb.cursor()
except mysql.connector.Error as err:
    logging.error(f"Error: {err}")
    exit(1)

# Function to validate the format of the number plate
def is_valid_number_plate(text):
    pattern = re.compile(r'^[A-Z0-9]{1,10}$')
    return pattern.match(text) is not None

# Initialize the video capture object
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    logging.error("Error: Could not open video capture.")
    exit(1)

# Continuously capture frames until a valid number plate is detected
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if frame is captured
    if not ret:
        logging.error("Error: Could not read frame.")
        break

    # Resizing image
    image = imutils.resize(frame, width=500)

    # Display the original frame
    cv2.imshow("Original Image", image)

    # Removing colors (grayscaling)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("1 - Grayscale Conversion", gray)

    # Apply bilateral filter to remove noise
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    cv2.imshow("2 - Bilateral Filter", gray)

    # Using canny edge detection
    edged = cv2.Canny(gray, 170, 200)
    cv2.imshow("4 - Canny Edges", edged)

    # Find contours
    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
    NumberPlateCnt = None

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            NumberPlateCnt = approx
            break

    # Check if a contour for the number plate is found
    if NumberPlateCnt is not None:
        # Masking the part other than the number plate
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [NumberPlateCnt], 0, 255, -1)
        new_image = cv2.bitwise_and(image, image, mask=mask)
        cv2.namedWindow("Final_image", cv2.WINDOW_NORMAL)
        cv2.imshow("Final_image", new_image)

        # Configuration for Tesseract
        configr = '-l eng --oem 1 --psm 7'

        # Run Tesseract OCR on image
        text = pytesseract.image_to_string(new_image, config=configr).strip().replace(" ", "")

        # Check if OCR extracted valid text and if the format matches a valid number plate
        if text and is_valid_number_plate(text):
            # Get current time (in_time)
            in_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            car_number = text

            try:
                # Check if the number plate already exists
                check_query = "SELECT * FROM in_time WHERE car_number = %s;"
                mycursor.execute(check_query, (car_number,))
                result = mycursor.fetchone()
                mycursor.fetchall()  # Fetch remaining results to clear the buffer

                if result:
                    # If exists, delete the old entry
                    delete_query = "DELETE FROM in_time WHERE car_number = %s;"
                    mycursor.execute(delete_query, (car_number,))
                    mydb.commit()
                    logging.info(f"Deleted old entry for car number {car_number}")

                # Insert the new entry
                insert_query = "INSERT INTO in_time (car_number, in_time) VALUES (%s, %s);"
                mycursor.execute(insert_query, (car_number, in_time))
                mydb.commit()
                logging.info(f"Inserted new entry for car number {car_number}")

                # Print recognized text and break the loop
                logging.info("Number plate is = %s", text)
                break

            except mysql.connector.Error as err:
                logging.error(f"Database error: {err}")

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
