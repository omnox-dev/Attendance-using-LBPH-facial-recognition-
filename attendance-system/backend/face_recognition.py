import cv2
import os
import numpy as np

TRAINER_PATH = os.path.join(os.path.dirname(__file__), 'trainer/trainer.yml')

def get_recognizer():
    """ Load or initialize LBPH face recognizer. """
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if os.path.exists(TRAINER_PATH):
        recognizer.read(TRAINER_PATH)
    return recognizer

def recognize_face(gray_frame, face_coords):
    """
    Recognize a single face from grayscale frame and its coordinates.
    Returns (predicted_id, confidence)
    """
    recognizer = get_recognizer()
    x, y, w, h = face_coords
    roi_gray = gray_frame[y:y+h, x:x+w]
    
    try:
        id, confidence = recognizer.predict(roi_gray)
        # Higher confidence in LBPH means lower accuracy. Typically < 100-110 is acceptable.
        if confidence < 100:
            return id, round(100 - confidence, 2)
        else:
            return "Unknown", round(100 - confidence, 2)
    except:
        return "Unknown", 0
