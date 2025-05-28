import cv2
import os

# Ask for the employee ID
employee_id = input("Enter Employee ID (e.g., E_01): ").strip()

# Create a directory for the employee if it doesn’t exist
save_path = f'dataset/{employee_id}'
os.makedirs(save_path, exist_ok=True)

# Load OpenCV's pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start the webcam
cap = cv2.VideoCapture(0)
count = 0
print("[INFO] Starting video stream. Look into the camera...")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grayscale, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        count += 1
        face_img = grayscale[y:y+h, x:x+w]
        face_filename = os.path.join(save_path, f'{employee_id}_{count}.jpg')
        cv2.imwrite(face_filename, face_img)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, f'Face {count}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    cv2.imshow('Capturing Faces (Press q to quit)', frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or count >= 100:
        break

cap.release()
cv2.destroyAllWindows()
print(f"[INFO] Finished capturing faces for {employee_id}.")
