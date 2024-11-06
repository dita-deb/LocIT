# Facial Recognition on Raspberry Pi Zero 2W
## Materials 
- Pi Zero 2W
- PiCamera Module 3
Arducam Multi-Camera Header
## Set Up Environment
### Install Despendencies
- sudo apt update
- sudo apt install python3-opencv python3-picamera2
## Code Files
- face_taker.py
- face_train.py
- face_recognizer.py
## Notes:
### Key Adjustments Summary
- Replaced cv2.VideoCapture with Picamera2 to utilize the Raspberry Pi Camera Module.
- Modified the image capture and display logic to ensure compatibility with the Pi’s performance limitations.

- Performance Optimization: Reduce the detectMultiScale parameters (scaleFactor and minNeighbors) if performance is slow.
- Testing: Test each script independently to ensure smooth functionality. The Raspberry Pi Zero 2 W has limited power, so patience and optimizations may be necessary.
