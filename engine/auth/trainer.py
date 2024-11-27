import cv2
import numpy as np
from PIL import Image  # Pillow package
import os

path = r'C:\Users\Rayan\Desktop\Jarvis\engine\auth\samples'  # Correct path to samples
recognizer = cv2.face.LBPHFaceRecognizer_create()  # Local Binary Patterns Histograms
detector = cv2.CascadeClassifier(r"C:\Users\Rayan\Desktop\Jarvis\engine\auth\haarcascade_frontalface_default.xml")  # Haar Cascade classifier

# Check if the classifier was loaded successfully
if detector.empty():
    print("Error: Haar Cascade classifier file not loaded.")
else:
    print("Haar Cascade classifier loaded successfully.")

def Images_And_Labels(path):  # Function to fetch the images and labels
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]     
    faceSamples = []
    ids = []

    for imagePath in imagePaths:  # To iterate through the particular image path
        gray_img = Image.open(imagePath).convert('L')  # Convert it to grayscale
        img_arr = np.array(gray_img, 'uint8')  # Create an array

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_arr)

        for (x, y, w, h) in faces:
            faceSamples.append(img_arr[y:y + h, x:x + w])
            ids.append(id)

    return faceSamples, ids

print("Training faces. It will take a few seconds. Wait...")

faces, ids = Images_And_Labels(path)
recognizer.train(faces, np.array(ids))

# Ensure the 'trainer' directory exists before saving the model
trainer_dir = r'engine\auth\trainer'
if not os.path.exists(trainer_dir):
    os.makedirs(trainer_dir)

# Use the absolute path for saving the trainer.yml
recognizer.write(r'C:\Users\Rayan\Desktop\Jarvis\engine\auth\trainer\trainer.yml')  # Save the trained model as trainer.yml

print("Model trained, now we can recognize your face.")
