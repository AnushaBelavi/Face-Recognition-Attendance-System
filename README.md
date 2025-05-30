## Face Recognition based Attendance Management System (FRAMS)
Face Recognition based Attendance Management System with a Flask web application and Power BI attendance dashboard.

### Table of Contents
- [Features](#features)
- [Youtube Demo](#youtube-demo)
- [Installation and Usage](#installation-and-usage)
- [Technologies Used](#technologies-used)
- [Methodology](#methodology)
- [User Interface Demo](#user-interface-demo)
- [License](#license)

### Features
- Face detection and recognition
- Attendance management
- Generates attendance reports in a csv file
- Secure admin login
- Interactive user interface
- Can detect multiple faces and mark attendance at a time 
- Works in bright and low light conditions
- Attendance dashboards using Power BI



### Installation and Usage
1. Clone the repository:
    ```
    git clone https://github.com/AnushaBelavi/Face-Recognition-Attendance-System.git
    ```
2. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Replace the training images with your own set of images in the folder `Training images`.
4. Open the `app.py` file and change the file paths as per your system.
5. Run the `app.py` file.

### Technologies Used
- **Programming Languages:** Python
- **Libraries:** OpenCV, dlib, face-recognition
- **Database:** SQLite
- **Web Application:** Flask, HTML, CSS, JavaScript
- **Data Visualization:** Power BI

### Methodology
- **Environment Setup:** Created a conda environment and installed necessary dependencies including OpenCV, dlib, face-recognition, and Flask.
- **Face Detection:** Converted images to black and white, then used HOG to detect faces by comparing image gradients.
- **Face Embedding:** Used 128-dimensional vectors and the triplet loss function for distinguishing between faces.
- **Face Recognition:** Utilized Euclidean distance with a threshold of 0.5 to compare the generated face encodings with the actual encodings of the training images to recognize the faces.
- **Database Connection:** Stored attendance data in a SQLite database and exported it to CSV for Power BI integration.
- **Web Application:** Developed a Flask-based web app for real-time attendance capturing and management.
- **Power BI Dashboard:** Connected the attendance data to Power BI to create dashboards. Embedded Power BI reports into the web app for real-time insights.





