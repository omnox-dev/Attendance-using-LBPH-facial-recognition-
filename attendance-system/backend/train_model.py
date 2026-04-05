import cv2
import os
import numpy as np
from PIL import Image

DATASET_PATH = os.path.join(os.path.dirname(__file__), 'dataset')
TRAINER_PATH = os.path.join(os.path.dirname(__file__), 'trainer/trainer.yml')

def train_lbph_model():
    """
    Trains LBPH face recognition model from images stored in dataset.
    Returns (num_faces, num_ids)
    """
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml'))

    image_paths = [os.path.join(DATASET_PATH, f) for f in os.listdir(DATASET_PATH) if f.startswith('User.')]
    
    face_samples = []
    ids = []

    for image_path in image_paths:
        # Load image and convert it to grayscale
        PIL_img = Image.open(image_path).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')

        # Get the student ID from filename (User.<id>.<count>.jpg)
        filename_parts = os.path.split(image_path)[-1].split('.')
        try:
           id = int(filename_parts[1])
           faces = detector.detectMultiScale(img_numpy)

           for (x, y, w, h) in faces:
               face_samples.append(img_numpy[y:y+h, x:x+w])
               ids.append(id)
        except Exception as e:
            print(f"Skipping {image_path}: {e}")
            continue

    if len(face_samples) == 0:
        return 0, 0

    recognizer.train(face_samples, np.array(ids))

    # Save the trained model to trainer/trainer.yml
    if not os.path.exists(os.path.dirname(TRAINER_PATH)):
        os.makedirs(os.path.dirname(TRAINER_PATH))
        
    recognizer.save(TRAINER_PATH)
    
    return len(face_samples), len(set(ids))
