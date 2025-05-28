from flask import Flask, render_template, request, session
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime, date
import sqlite3
import json
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load known images and encodings once at startup
path = 'Training images'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            encodeList.append(encodings[0])
    return encodeList

encodeListKnown = findEncodings(images)

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == "POST":
        return render_template('index.html')
    else:
        return "Everything is okay!"

@app.route('/name', methods=['GET', 'POST'])
def name():
    if request.method == "POST":
        name1 = request.form['name1']
        name2 = request.form['name2']

        # Use mobile camera stream here
        cam = cv2.VideoCapture("http://192.168.23.86:8080/video")

        while True:
            ret, frame = cam.read()
            if not ret:
                print("Failed to grab frame")
                break
            cv2.imshow("Press Space to capture image", frame)

            k = cv2.waitKey(1)
            if k % 256 == 27:
                print("Escape hit, closing...")
                break
            elif k % 256 == 32:
                img_name = name1 + ".png"
                path = 'D:/BACKUP 21-10-2021/LOCAL DISK -D/FRAMS2/Training images'
                cv2.imwrite(os.path.join(path, img_name), frame)
                print(f"{img_name} written!")

        cam.release()
        cv2.destroyAllWindows()
        return render_template('image.html')
    else:
        return 'All is not well'

@app.route("/", methods=["GET", "POST"])
def recognize():
    if request.method == "POST":

        def markData(name):
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            today = date.today()
            conn = sqlite3.connect('information.db')
            conn.execute('''CREATE TABLE IF NOT EXISTS Attendance
                            (NAME TEXT NOT NULL, Time TEXT NOT NULL, Date TEXT NOT NULL)''')
            conn.execute("INSERT OR IGNORE INTO Attendance (NAME, Time, Date) VALUES (?, ?, ?)",
                         (name, dtString, today))
            conn.commit()
            conn.close()

        def markAttendance(name):
            now = datetime.now()
            dtString = now.strftime('%Y-%m-%d %H:%M:%S')
            with open('attendance.csv', 'a+', errors='ignore') as f:
                f.seek(0)
                myDataList = f.readlines()
                nameList = [line.split(',')[0] for line in myDataList]
                if name not in nameList:
                    f.writelines(f'\n{name},{dtString}')

        cap = cv2.VideoCapture("http://192.168.23.86:8080/video")

        while True:
            success, img = cap.read()
            if not success:
                break
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)

                name = 'Unknown'
                if faceDis[matchIndex] < 0.50:
                    name = classNames[matchIndex].upper()
                    markAttendance(name)
                    markData(name)

                y1, x2, y2, x1 = [v * 4 for v in faceLoc]
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow('Punch your Attendance', img)
            if cv2.waitKey(1) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

        return render_template('first.html')
    else:
        return render_template('main.html')

@app.route('/login', methods=['POST'])
def login():
    json_data = json.loads(request.data.decode())
    username = json_data['username']
    password = json_data['password']
    df = pd.read_csv('cred.csv')
    user_match = df.loc[df['username'] == username]
    if not user_match.empty and user_match['password'].values[0] == password:
        session['username'] = username
        return 'success'
    return 'failed'

@app.route('/checklogin')
def checklogin():
    return session.get('username', 'False')

@app.route('/how', methods=["GET", "POST"])
def how():
    return render_template('form.html')

@app.route('/data', methods=["GET", "POST"])
def data():
    if request.method == "POST":
        today = date.today()
        conn = sqlite3.connect('information.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cursor = cur.execute("SELECT DISTINCT NAME, Time, Date FROM Attendance WHERE Date=?", (today,))
        rows = cur.fetchall()
        conn.close()
        return render_template('form2.html', rows=rows)
    else:
        return render_template('form1.html')

@app.route('/whole', methods=["GET", "POST"])
def whole():
    conn = sqlite3.connect('information.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cursor = cur.execute("SELECT DISTINCT NAME, Time, Date FROM Attendance")
    rows = cur.fetchall()
    conn.close()
    return render_template('form3.html', rows=rows)

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
