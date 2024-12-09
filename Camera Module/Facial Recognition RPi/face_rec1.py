#!/usr/bin/python3

import cv2
import os
import time
from picamera2 import Picamera2


# Download the cascade file from the link below
# https://github.com/opencv/opencv/blob/4.x/data/haarcascades/haarcascade_frontalface_default.xml

face_detector = cv2.CascadeClassifier("/home/pi/Face Recognition/haarcascade_frontalface_default.xml")
cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

# Create a directory to store detected faces
output_directory = "detected_faces"
os.makedirs(output_directory, exist_ok=True)

# Create a dictionary to store the name and corresponding face images
face_database = {}

while True:
    im = picam2.capture_array()

    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(grey, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0))

        # Prompt the user for their name if it's the first face detected
        if len(face_database) == 0:
            name = input("Please enter your name for this face: ")
            face_database[name] = []

        # Generate a unique filename using timestamp for every saved image
        timestamp = int(time.time())
        filename = os.path.join(output_directory, f"{name}_face_{timestamp}.jpg")
        cv2.imwrite(filename, im[y:y+h, x:x+w])  # Save only the detected face portion

        # Store the face image in the database for the given name
        face_database[name].append(filename)

    cv2.imshow("Camera", im)
    cv2.waitKey(1)

