# importing libraries
import time

import cv2
import imutils
import mysql.connector
import numpy as np
import pandas as pd
import pytesseract

# Using SQL for database management

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="spms"
)
mycursor = mydb.cursor()

# reading image with help of cv2 library
# image = cv2.imread('D8.jpeg')
# image = cv2.imread('MH 12 DE 1433.jpg')
image = cv2.imread('swift no palte.jpg')
# resizing image
image = imutils.resize(image, width=500)

cv2.imshow("Original Image", image)
# removing colours (grayscaling)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("1 - Grayscale Conversion", gray)

gray = cv2.bilateralFilter(gray, 11, 17, 17)
cv2.imshow("2 - Bilateral Filter", gray)
# using canny edge detection
edged = cv2.Canny(gray, 170, 200)
cv2.imshow("4 - Canny Edges", edged)

cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
NumberPlateCnt = None

count = 0
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 4:
        NumberPlateCnt = approx
        break

# Masking the part other than the number plate
mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [NumberPlateCnt], 0, 255, -1)
new_image = cv2.bitwise_and(image, image, mask=mask)
cv2.namedWindow("Final_image", cv2.WINDOW_NORMAL)
cv2.imshow("Final_image", new_image)

# Configuration for tesseract
configr = ('-l eng --oem 1 --psm 7')

# Run tesseract OCR on image
text = pytesseract.image_to_string(new_image, config=configr)

# Data is stored
raw_data = {'date & time ': [time.asctime(time.localtime(time.time()))],
            'v_number': [text]}

df = pd.DataFrame(raw_data, columns=['date & time ', 'v_number'])

# Time on which car is getting in and storing in SQL database
date_time = time.asctime(time.localtime(time.time()))
car_number = text
values = (date_time, car_number)
insert = "insert into in_time values(%s,%s);"
mycursor.execute(insert, values)

mycursor.execute("select * from in_time;")
out = mycursor.fetchall()
print(date_time, end='\t\t')
print(car_number)
mydb.commit()

# Print recognized text
print("no. plate is =", text)
# cv2.waitKey(0)
