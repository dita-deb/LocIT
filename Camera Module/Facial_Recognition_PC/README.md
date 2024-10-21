# Facial Recognition on VSCode
## Milestone #1 Demo

### Overview:
This folder contains the code used for facial recognition tasks, specifically capturing, training, and recognizing faces.

### Week 6 Code:
#### File Descriptions:
Face_taker.py: Captures images of the target individual and stores them in the dataset for later use in training the model.

Face_train.py: Trains the facial recognition model using the images captured in Face_taker.py, allowing the system to recognize the individual’s face.

face_recognizer.py: Runs the trained facial recognition model, identifying individuals from the dataset in real-time or from new images.

names.json: Stores a mapping between each individual's name and their corresponding image data in the dataset.

haarcascade_frontalface_default.xml: A pre-trained Haar Cascade classifier that detects facial features (e.g., eyes, nose, mouth) to identify and classify faces for recognition.

### Videos:
![NotWorking_with_Sister-ezgif com-crop](https://github.com/user-attachments/assets/479a4cb3-6d5d-4170-b0b5-bd5a3a324527)
This video is from when the model was not working and giving an error when tracking multiple faces to the same name.

![Working_with_Roommate-ezgif com-crop](https://github.com/user-attachments/assets/0ab66e87-168d-4959-8fcc-bceb19e80f09)
This video is from the model starts recognizing two people accurately.
