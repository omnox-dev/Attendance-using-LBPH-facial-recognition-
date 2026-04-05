import cv2
import os

HAAR_CASCADE_PATH = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml')

def detect_faces(frame):
    """
    Detects faces in a frame using Haar Cascade with optimized search scale.
    """
    face_cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    # Optimization: Resize frame to half width for faster detection
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
    
    # Increase minSize and adjust scaleFactor for more speed
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(40, 40))
    
    face_data = []
    for (x, y, w, h) in faces:
        # Scale coordinates back up to original frame size
        face_data.append((x*2, y*2, w*2, h*2))
        cv2.rectangle(frame, (x*2, y*2), ((x+w)*2, (y+h)*2), (255, 0, 0), 2)
        
    return frame, face_data, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
