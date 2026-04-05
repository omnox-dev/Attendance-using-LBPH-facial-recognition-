import cv2
import os
import time

DATASET_PATH = os.path.join(os.path.dirname(__file__), 'dataset')
HAAR_CASCADE_PATH = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml')

def capture_student_images(student_id):
    """
    Captures 20-30 images of a student from webcam for training.
    Saves them in dataset/ with filename format User.<id>.<count>.jpg
    """
    if not os.path.exists(DATASET_PATH):
        os.makedirs(DATASET_PATH)

    camera = cv2.VideoCapture(0)
    face_detector = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    
    count = 0
    print(f"Starting image collection for Student ID: {student_id}")
    
    while True:
        ret, frame = camera.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            
            # Save the captured face image to dataset folder
            img_name = f"User.{student_id}.{count}.jpg"
            img_path = os.path.join(DATASET_PATH, img_name)
            cv2.imwrite(img_path, gray[y:y+h, x:x+w])

            cv2.putText(frame, f"Captured: {count}/30", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Registration - Stay still...', frame)

        if cv2.waitKey(100) & 0xFF == 27: # Press Escape to quit early
            break
        elif count >= 30: # Capture 30 images
             break

    camera.release()
    cv2.destroyAllWindows()
    return count
