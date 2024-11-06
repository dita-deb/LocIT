import cv2
import numpy as np
import json
import os
from picamera2 import Picamera2

if __name__ == "__main__":
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer.yml')
    face_cascade_Path = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(face_cascade_Path)
    font = cv2.FONT_HERSHEY_SIMPLEX

    with open('names.json', 'r') as fs:
        names = json.load(fs)
        names = list(names.values())

    picam = Picamera2()
    picam.start()
    minW, minH = 64, 48

    while True:
        frame = picam.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH))
        )
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            name = names[id] if confidence > 51 else "Who are you?"
            conf_text = f"  {round(confidence)}%" if confidence > 51 else "N/A"
            
            cv2.putText(frame, name, (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(frame, conf_text, (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
        
        cv2.imshow('camera', frame)
        if cv2.waitKey(10) & 0xFF == 27:  # Press Escape to exit
            break

    print("\n[INFO] Exiting Program.")
    picam.close()
    cv2.destroyAllWindows()
