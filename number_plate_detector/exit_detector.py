import time
import cv2
import imutils
import mysql.connector
import numpy as np
import pytesseract
import re
from datetime import datetime

# Connect to SQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="spms"
)
mycursor = mydb.cursor()

# Function to validate the number plate format
def is_valid_number_plate(text):
    pattern = re.compile(r'^[A-Z0-9]{1,10}$')
    return pattern.match(text) is not None

# Initialize video capture
cap = cv2.VideoCapture(0)

# Continuously capture frames
while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Resizing image
    image = imutils.resize(frame, width=500)

    # Display original frame
    cv2.imshow("Original Image", image)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("1 - Grayscale Conversion", gray)

    # Apply bilateral filter to remove noise
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    cv2.imshow("2 - Bilateral Filter", gray)

    # Apply Canny edge detection
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
        # Mask the part other than the number plate
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [NumberPlateCnt], 0, 255, -1)
        new_image = cv2.bitwise_and(image, image, mask=mask)
        cv2.namedWindow("Final_image", cv2.WINDOW_NORMAL)
        cv2.imshow("Final_image", new_image)

        # Configure tesseract
        configr = '-l eng --oem 1 --psm 7'

        # Run tesseract OCR on image
        text = pytesseract.image_to_string(new_image, config=configr).strip().replace(" ", "")

        # Check if OCR extracted valid text and if the format matches a valid number plate
        if text and is_valid_number_plate(text):
            # Get current time (exit time)
            date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Correct MySQL format
            car_number = text

            # Check if the number plate exists in the database
            check_query = "SELECT in_time FROM in_time WHERE car_number = %s;"
            mycursor.execute(check_query, (car_number,))
            result = mycursor.fetchone()

            if result:
                # Convert the in_time from database into datetime format
                in_time = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
                out_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                duration = (out_time - in_time).total_seconds() / 60  # duration in minutes

                # Calculate price (assuming a rate of 1 rupee per minute)
                price = duration * 1

                # Print details in the terminal
                print(f"Exit Time: {date_time}")
                print(f"Duration: {duration:.2f} minutes")
                print(f"Price for the stay: {price:.2f} rupees")

                # Remove the car entry from the in_time table
                delete_query = "DELETE FROM in_time WHERE car_number = %s;"
                mycursor.execute(delete_query, (car_number,))
                mydb.commit()

                # Insert record into the records table
                insert_query = "INSERT INTO records (car_number, in_time, out_time, duration, price) VALUES (%s, %s, %s, %s, %s);"
                mycursor.execute(insert_query, (car_number, result[0], date_time, duration, price))
                mydb.commit()

                print(f"Record inserted into the records table for car number {car_number}")

            else:
                print(f"No entry found for car number {car_number}")

            # Print recognized text (number plate)
            print(f"Number plate is = {text}")
            break

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
