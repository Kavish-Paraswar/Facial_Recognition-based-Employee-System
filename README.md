# Facial Recognition Employee System

AI-based attendance system using real-time facial recognition with LBPH.

![Dashboard](https://github.com/user-attachments/assets/741fd792-b6de-4a8f-a24f-314dca279771)

Built with Flask, OpenCV, and SQLite for secure, contactless employee tracking.

## 🚀 Features

- Real-time facial recognition using webcam
- LBPH algorithm for accurate identification
- Haar Cascade for face detection
- Role-based dashboard for Admins and Employees
- Secure login and profile management
- Attendance logging with date & time
- SQLite database for structured storage
- Responsive web interface with Flask

---

## 🛠 Tech Stack

- **Frontend**: HTML, CSS
- **Backend**: Python (Flask)
- **Face Detection**: OpenCV + Haar Cascade
- **Facial Recognition**: LBPH algorithm (OpenCV)
- **Database**: SQLite

---
## Images 
![Screenshot 2025-05-28 114701](https://github.com/user-attachments/assets/741fd792-b6de-4a8f-a24f-314dca279771)
Fig - 1

![Screenshot 2025-05-28 114604](https://github.com/user-attachments/assets/5c74c457-e2c6-432c-94af-b6877e756c8b)
Fig - 2


## 📁 Project Structure

├── app.py # Main Flask application

├── static/ # CSS/JS files

├── templates/ # HTML templates

├── dataset/ # Stored face images

├── trainer/ # LBPH trained model

├── attendance.db # SQLite database file


---

## 🧑‍💻 How to Run

1. Clone the repo  
2. Install dependencies: `pip install -r requirements.txt`  
3. Run the app: `python app.py`  
4. Open browser: `http://localhost:5000`

---

## 📸 Face Registration & Attendance

- Admin registers employee with face data.
- LBPH model is trained on captured images.
- System recognizes faces in real-time and logs attendance.

---

## 📌 Future Improvements

- Cloud storage integration
- Mobile app access
- Anti-spoofing measures
- Advanced analytics dashboard

---

## 👥 Authors

- Kavish Paraswar  
- Prachi Pawar  
- Swaraj Patil  
- Riddhi Patel  

---



