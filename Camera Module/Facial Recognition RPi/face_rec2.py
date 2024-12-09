#!/usr/bin/python3

import cv2
import os
import numpy as np
from picamera2 import Picamera2

# Load the face detector
face_detector = cv2.CascadeClassifier("/home/pi/Face Recognition/haarcascade_frontalface_default.xml")
cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

# Load the face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Create a dictionary to store the names and associated face IDs
name_mapping = {}
face_images = []
face_labels = []

# Function to load the faces from the detected_faces folder and train the recognizer
def load_face_database():
    # Check if the directory exists
    if not os.path.exists("detected_faces"):
        print("Error: detected_faces directory not found.")
        return False

    # Process each image in the directory
    for filename in os.listdir("detected_faces"):
        if filename.endswith(".jpg"):
            print(f"Processing file: {filename}")
            img = cv2.imread(os.path.join("detected_faces", filename), cv2.IMREAD_GRAYSCALE)
            
            if img is None:
                print(f"Error: Unable to read {filename}")
                continue
            
            # Extract the name from the filename (assuming "name_face_timestamp.jpg")
            name = filename.split('_')[0]
            
            # Add the image and label to the training data
            face_images.append(img)
            face_labels.append(len(name_mapping))
            name_mapping[len(name_mapping)] = name  # Map the label index to the name

    # Check if we have any valid images
    if len(face_images) == 0 or len(face_labels) == 0:
        print("Error: No valid face images found in detected_faces.")
        return False

    # Train the recognizer with the collected face images
    recognizer.train(face_images, np.array(face_labels))
    print(f"Face recognizer trained successfully with {len(face_images)} images.")
    return True

# Load the face database (train the recognizer)
if not load_face_database():
    print("Face database loading failed. Exiting.")
    exit(1)

while True:
    im = picam2.capture_array()
    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(grey, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0))

        # Get the face region
        face_region = grey[y:y+h, x:x+w]
        
        try:
            # Predict the label for the detected face
            label, confidence = recognizer.predict(face_region)

            # Display the name of the person if the confidence is high enough
            if confidence < 100:  # Adjust threshold based on your needs
                name = name_mapping[label]
                cv2.putText(im, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(im, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        except Exception as e:
            print(f"Prediction error: {e}")
            cv2.putText(im, "Error", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the camera feed
    cv2.imshow("Face Recognition", im)

    # Exit the loop if 'ESC' is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
