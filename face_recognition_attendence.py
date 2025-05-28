import cv2
import numpy as np
import os
from datetime import datetime
import csv
from flask_sqlalchemy import SQLAlchemy
from app import app, db, Employee  # assuming your Flask app is in app.py
from app import Employee  # import your model

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/face_trainer.yml')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

font = cv2.FONT_HERSHEY_SIMPLEX
attendance_file = f"Attendance/attendance_{datetime.now().strftime('%Y-%m-%d')}.csv"

# Create attendance CSV for today if not exists
if not os.path.exists(attendance_file):
    with open(attendance_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Employee ID', 'Name', 'Time'])

def mark_attendance(emp_id, name):
    with open(attendance_file, 'r+') as f:
        data = f.readlines()
        existing_ids = [line.split(',')[0] for line in data]
        if emp_id not in existing_ids:
            now = datetime.now()
            time_string = now.strftime('%H:%M:%S')
            f.writelines(f'\n{emp_id},{name},{time_string}')
            print(f"[INFO] Attendance marked for {name} ({emp_id})")

cam = cv2.VideoCapture(0)

print("[INFO] Starting face recognition. Press Q to quit.")
while True:
    ret, img = cam.read()
    if not ret:
        print("[ERROR] Failed to access webcam.")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)

    for (x, y, w, h) in faces:
        face_id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        if confidence < 70:
            emp_id = f"E_{face_id:02d}"
            with app.app_context():
               employee = Employee.query.filter_by(employee_id=emp_id).first()


            if employee:
                name = employee.name
                cv2.putText(img, f"{name}", (x+5, y-5), font, 1, (0, 255, 0), 2)
                mark_attendance(emp_id, name)
            else:
                cv2.putText(img, "Unknown", (x+5, y-5), font, 1, (0, 0, 255), 2)
        else:
            cv2.putText(img, "Unknown", (x+5, y-5), font, 1, (0, 0, 255), 2)

        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('Attendance', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
