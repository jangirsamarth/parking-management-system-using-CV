🚗 Parking Management System Using Computer Vision 🅿️
Table of Contents
Introduction
Features
Technologies Used
Installation
Usage
Project Structure
Contributing
License
Contact
Introduction
The Parking Management System Using Computer Vision leverages advanced computer vision and machine learning techniques to automate the detection and tracking of vehicles in parking spaces. This system streamlines parking management, reduces human error, and enhances the overall efficiency of parking facilities.

Features
Automated Number Plate Recognition (ANPR): Detects and reads vehicle number plates using OCR.
Real-time Tracking: Monitors vehicle entry and exit times.
Database Integration: Stores and manages parking data in a MySQL database.
Cost Calculation: Computes the parking fee based on the duration of stay.
User-Friendly Interface: Displays real-time video feed and processing steps.
Technologies Used
Programming Languages: Python
Computer Vision Libraries: OpenCV, cv2, cvzone
OCR: pytesseract
Database: MySQL
Others: NumPy, pillow, re
Installation
Follow these steps to set up the Parking Management System on your local machine.

Prerequisites
Python 3.12 or higher
MySQL
VS code or any other preferred IDE
Clone the Repository
bash
Copy code
git clone https://github.com/jangirsamarth/parking-management-system-using-CV.git
cd parking-management-system-using-CV
Install Dependencies
bash
Copy code
pip install opencv-python opencv-python-headless cvzone pytesseract mysql-connector-python pillow
Project Structure
Create two folders:

parking_space_detector: For detection of parking spaces.
Put main.py and parking_space_detector_2.py in this folder.
billing_system: For number plate detection and other functions.
Put entry_detector.py and exit_detector.py in this folder.
Install pytesseract in the same folder as entry_detector.py and exit_detector.py as the codes will only run when it is installed this way.
Configure the Database:

Setup MySQL and change your password in entry_detector.py and exit_detector.py.
Import SQL files into the MySQL workbench and name the database smps.
Links for Dependencies
pytesseract
MySQL
IntelliJ IDEA
Usage
Video Feed Setup:

Give a video feed to main.py and take a proper screenshot from the video feed to use in parking_space_detector_2.py.
Run the Parking Space Detector:

Execute parking_space_detector_2.py and carefully create the windows (boxes) in which parking space will be detected.
Adjust the size of the boxes in the code through trial and error to achieve perfect boxes.
Run the Main Script:

Make sure to input the exact same dimensions of boxes in main.py.
Run main.py to see the efficiency of parking space detection.
Database Connection:

Ensure the database is connected via MySQL connector.
Run Entry and Exit Detectors:

Run entry_detector.py to detect vehicle entry.
Run exit_detector.py to detect vehicle exit and calculate the parking fee.
Contributing
We welcome contributions to enhance the Parking Management System. To contribute, follow these steps:

Fork the repository.
Create a new branch for your feature or bugfix.
Make your changes and commit them.
Push your changes to your fork.
Create a pull request to the main repository.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
Feel free to reach out for any questions or collaborations:

Email: samarth8947@gmail.com
LinkedIn: Samarth Jangir
