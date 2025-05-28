import cv2
import numpy as np
import os
from PIL import Image

# Path to the dataset
dataset_path = 'dataset'
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def get_images_and_labels(path):
    face_samples = []
    ids = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("jpg") or file.endswith("png"):
                image_path = os.path.join(root, file)
                PIL_img = Image.open(image_path).convert('L')  # convert to grayscale
                img_numpy = np.array(PIL_img, 'uint8')

                # Extract employee ID (folder name)
                id_str = os.path.basename(root)
                id_numeric = int(id_str.split("_")[1])  # E_01 → 1
                faces = detector.detectMultiScale(img_numpy)

                for (x, y, w, h) in faces:
                    face_samples.append(img_numpy[y:y+h, x:x+w])
                    ids.append(id_numeric)

    return face_samples, ids

print("[INFO] Training the model. Please wait...")
faces, ids = get_images_and_labels(dataset_path)
recognizer.train(faces, np.array(ids))

# Save the model into trainer/
os.makedirs('trainer', exist_ok=True)
recognizer.write('trainer/face_trainer.yml')
print(f"[INFO] {len(set(ids))} employee(s) trained. Model saved as 'trainer/face_trainer.yml'.")
