# importing libraries
import time

import cv2
import imutils
import mysql.connector
import numpy as np
import pandas as pd
import pytesseract

# using SQL for database management


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="spms"
)
mycursor = mydb.cursor()


# Time converter functions

def sec_to_min(time_stayed):
    temp = time_stayed
    time_stayed = time_stayed // 60
    temp = temp - time_stayed * 60
    stayed_min = time_stayed
    stayed_sec = temp
    return stayed_min, stayed_sec


def sec_to_hour(time):
    temp = time
    time = time // 3600
    temp = temp - time * 3600
    stayed_hour = time
    return stayed_hour, temp


# Cost calculator function
def cost(stayed_time):
    hours = stayed_time / 3600
    cost = hours * 60
    return cost


# reading image with help of cv2 library
# image = cv2.imread('D8.jpeg')
image = cv2.imread('swift no palte.jpg')
# image = cv2.imread('MH 12 DE 1433.jpg')

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
configr = '-l eng --oem 1 --psm 7'

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
insert = "insert into out_time values(%s,%s);"
mycursor.execute(insert, values)

mycursor.execute("select * from out_time;")
out = mycursor.fetchall()
mydb.commit()

# Print recognized text
print("no. plate is =", text)

mycursor.execute("select * from out_time;")
out = mycursor.fetchall()
print(date_time, end='\t\t')
print(car_number)
mydb.commit()

car_number = (text,)
output = "select in_time.in_time,in_time.car_number,out_time.out_time from in_time, out_time where in_time.car_number=out_time.car_number and in_time.car_number=%s;"
mycursor.execute(output, car_number)
output = mycursor.fetchall()

# code to check if the no. plate scanned is in the database
# if there is one then generating bill on the time car stayed in the parking lot
# for references we have chosen 60 rupees per hour

mydb.commit()
if output == []:
    print('INVALID INPUT')

# print("In date and time: ")
in_date = int(output[0][0][8:10])
in_hour = int(output[0][0][11:13])
in_min = int(output[0][0][14:16])
in_sec = int(output[0][0][17:19])

# print("Out date and time: ")
out_date = int(output[0][2][8:10])
out_hour = int(output[0][2][11:13])
out_min = int(output[0][2][14:16])
out_sec = int(output[0][2][17:19])

if in_date == out_date:
    in_time = (in_hour * 3600) + (in_min * 60) + in_sec
    out_time = (out_hour * 3600) + (out_min * 60) + out_sec
    time_stayed = out_time - in_time
    if 59 < time_stayed < 3600:
        stayed_min, stayed_sec = sec_to_min(time_stayed)
        print("The time for which the car stayed = ", stayed_min, "minutes", stayed_sec, "seconds")
        print("Price for the stay", cost(time_stayed))
    elif time_stayed > 3599:
        stayed_hour, temp = sec_to_hour(time_stayed)
        stayed_min, stayed_sec = sec_to_min(temp)
        print("The time for which the car stayed = ", stayed_hour, "hours", stayed_min, "minutes", stayed_sec,
              "seconds")
        print("Price for the stay", cost(time_stayed))
    else:
        print("The time for which the car stayed = ", time_stayed, "seconds")
        print("Price for the stay", cost(time_stayed))
else:
    if in_date == out_date - 1:
        in_time = (in_hour * 3600) + (in_min * 60) + in_sec
        out_time = (out_hour * 3600) + (out_min * 60) + out_sec
        time_stayed_temp = 24 * 3600 - in_time
        time_stayed_temp_1 = out_time - 0
        time_stayed = time_stayed_temp + time_stayed_temp_1
        if 59 < time_stayed < 3600:
            stayed_min, stayed_sec = sec_to_min(time_stayed)
            print("The time for which the car stayed = ", stayed_min, "minutes", stayed_sec, "seconds")
            print("Price for the stay", cost(time_stayed))
        elif time_stayed > 3600:
            stayed_hour, temp = sec_to_hour(time_stayed)
            stayed_min, stayed_sec = sec_to_min(temp)
            print("The time for which the car stayed = ", stayed_hour, "hours", stayed_min, "minutes", stayed_sec,
                  "seconds")
            print("Price for the stay", cost(time_stayed))
        else:
            print("The time for which the car stayed = ", time_stayed, "seconds")
            print("Price for the stay", cost(time_stayed))
    elif in_date < out_date - 1:
        stayed_days = out_date - 1 - in_date
        in_time = (in_hour * 3600) + (in_min * 60) + in_sec
        out_time = (out_hour * 3600) + (out_min * 60) + out_sec
        time_stayed_temp = 24 * 3600 - in_time
        time_stayed_temp_1 = out_time - 0
        time_stayed = time_stayed_temp + time_stayed_temp_1
        if 59 < time_stayed < 3600:
            stayed_min, stayed_sec = sec_to_min(time_stayed)
            print("The time for which the car stayed = ", stayed_min, "minutes", stayed_sec, "seconds")
            print("Price for the stay", cost(time_stayed))
        elif time_stayed > 3600:
            stayed_hour, temp = sec_to_hour(time_stayed)
            stayed_min, stayed_sec = sec_to_min(temp)
            print("The time for which the car stayed = ", stayed_days, "days", stayed_hour, "hours", stayed_min,
                  "minutes", stayed_sec, "seconds")
            print("Price for the stay", cost(time_stayed))
        else:
            print("The time for which the car stayed = ", time_stayed, "seconds")
            print("Price for the stay", cost(time_stayed))
