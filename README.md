

# 🚗🅿️ Parking Management System Using Computer Vision

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Streamlit Dashboard](#streamlit-dashboard)
8. [Contributing](#contributing)
9. [License](#license)
10. [Contact](#contact)

## Introduction
The Parking Management System Using Computer Vision is designed to automate parking spot detection and billing with advanced computer vision techniques. It streamlines parking management, minimizes human error, and enhances the efficiency of parking facilities by integrating real-time vehicle number plate recognition, automated billing, and accurate data management.

## Features
- **Automated Number Plate Recognition (ANPR)**: Uses Optical Character Recognition (OCR) to detect and read vehicle number plates.
- **Real-time Tracking**: Monitors and logs vehicle entry and exit times.
- **Database Integration**: Manages and stores parking data in a MySQL database.
- **Cost Calculation**: Computes parking fees based on the duration of stay, reducing human interaction by 90% and expediting the billing process by 50%.
- **User-Friendly Interface**: Provides a real-time video feed and displays processing steps via a Streamlit dashboard.

## Technologies Used
- **Programming Languages**: Python
- **Computer Vision Libraries**: OpenCV, cv2, cvzone
- **OCR Library**: pytesseract
- **Database**: MySQL
- **Others**: NumPy, Pillow, re
- **Dashboard**: Streamlit

## Installation
Follow these steps to set up the Parking Management System on your local machine.

### Prerequisites
- Python 3.12 or higher
- MySQL
- Preferred IDE (e.g., IntelliJ IDEA)
- Streamlit

### Clone the Repository
```bash
git clone https://github.com/jangirsamarth/parking-management-system-using-CV.git
cd parking-management-system-using-CV
```

### Install Dependencies
```bash
pip install -r requirements.txt
pip install streamlit
```

## Project Structure
Organize the project into the following folders:

- **parking_space_detector**: Contains scripts for parking space detection.
  - `main.py`: Main script for parking space detection.
  - `parking_space_detector_2.py`: Helper script for configuring parking spaces.
- **billing_system**: Contains scripts for number plate detection and fee calculation.
  - `entry_detector.py`: Detects vehicle entry and logs data.
  - `exit_detector.py`: Detects vehicle exit and calculates parking fees.
- **dashboard**: Contains the Streamlit dashboard for visualizing parking data.
  - `dashboard.py`: Displays vehicle data, parking duration, and costs in real-time.

Ensure `pytesseract` is installed in the same directory as `entry_detector.py` and `exit_detector.py`.

### Configure the Database
- Set up MySQL and update the password in `entry_detector.py` and `exit_detector.py`.
- Import SQL files into MySQL Workbench and create a database named `smps`.

## Usage

### Video Feed Setup
- Provide a video feed to `main.py` and capture an appropriate screenshot for use in `parking_space_detector_2.py`.

### Run the Parking Space Detector
- Execute `parking_space_detector_2.py` to create and configure parking spot windows.
- Adjust box dimensions through trial and error to ensure accurate detection.

### Run the Main Script
- Input the exact dimensions of the boxes in `main.py` to match those configured in `parking_space_detector_2.py`.
- Run `main.py` to test and evaluate parking space detection.

### Database Connection
- Ensure the database is connected using the MySQL connector.

### Run Entry and Exit Detectors
- Execute `entry_detector.py` to detect vehicle entries.
- Execute `exit_detector.py` to handle vehicle exits and calculate fees.

### Streamlit Dashboard
- To launch the Streamlit dashboard, run:
  ```bash
  streamlit run dashboard/dashboard.py
  ```
- The dashboard will display real-time data including vehicle details, parking duration, and cost, providing a comprehensive view of parking management.

## Contributing
Contributions to enhance the Parking Management System are welcome. To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make changes and commit them.
4. Push changes to your fork.
5. Create a pull request to the main repository.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or collaboration:
- Email: [samarth8947@gmail.com](mailto:samarth8947@gmail.com)
- LinkedIn: [Samarth Jangir](https://www.linkedin.com/in/samarth-jangir)

---
