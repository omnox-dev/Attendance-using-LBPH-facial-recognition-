from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy.orm import Session
from database import get_db, engine
import models
from train_model import train_lbph_model
from register_student import capture_student_images
from attendance_service import mark_attendance, export_attendance_csv
import cv2
import os

app = FastAPI(title="Face Recognition Attendance System API")

# Update CORS to be more specific and robust
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Attendance System API Started"}

@app.post("/register-student")
def register_student(name: str, roll_number: str, db: Session = Depends(get_db)):
    # Check if student already exists
    existing = db.query(models.Student).filter(models.Student.roll_number == roll_number).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Roll Number {roll_number} already registered.")
    
    new_student = models.Student(name=name, roll_number=roll_number)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    # Trigger Webcam for image collection
    capture_student_images(new_student.id)

    return {"message": f"Successfully registered Student ID: {new_student.id}.", "student": new_student}

@app.post("/train-model")
def train_model():
    num_faces, num_ids = train_lbph_model()
    if num_faces == 0:
        raise HTTPException(status_code=400, detail="No student images found for training.")

    return {"message": f"Training completed. {num_faces} faces processed for {num_ids} students.", "status": "Trainer updated."}

@app.get("/attendance")
def get_attendance_log(db: Session = Depends(get_db)):
    records = db.query(models.Attendance).join(models.Student).all()
    
    results = []
    for record in records:
        results.append({
            "id": record.id,
            "name": record.student.name,
            "roll_number": record.student.roll_number,
            "date": str(record.date),
            "time": str(record.time),
            "status": record.status
        })
    return results

@app.get("/export-csv")
def download_csv(db: Session = Depends(get_db)):
    csv_data = export_attendance_csv(db)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=attendance_report.csv"}
    )

@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Delete related attendance records first
    db.query(models.Attendance).filter(models.Attendance.student_id == student_id).delete()
    
    # Delete student from DB
    db.delete(student)
    db.commit()

    # Optional: Clean up images from dataset folder
    dataset_path = os.path.join(os.path.dirname(__file__), 'dataset')
    if os.path.exists(dataset_path):
        for f in os.listdir(dataset_path):
            if f.startswith(f"User.{student_id}."):
                os.remove(os.path.join(dataset_path, f))

    return {"message": f"Student {student_id} and all related data deleted successfully"}

from fastapi.responses import Response, StreamingResponse
from sqlalchemy.orm import Session
import asyncio

# Global variable to control camera state for web streaming
camera_active = False

def generate_frames(db: Session):
    global camera_active
    from face_detection import detect_faces
    from face_recognition import recognize_face
    
    camera = cv2.VideoCapture(0)
    student_map = {s.id: s.name for s in db.query(models.Student).all()}
    
    while camera_active:
        success, frame = camera.read()
        if not success:
            break
        
        # Detect faces
        frame, detections, gray_frame = detect_faces(frame)
        
        for (x, y, w, h) in detections:
            student_id, confidence = recognize_face(gray_frame, (x, y, w, h))

            if student_id != "Unknown":
                name = student_map.get(student_id, f"ID: {student_id}")
                mark_attendance(db, student_id)
                cv2.putText(frame, f"{name}: {confidence}%", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    camera.release()

@app.get("/video-feed")
def video_feed(db: Session = Depends(get_db)):
    global camera_active
    if not camera_active:
        return Response(status_code=404, content="Camera not started")
    return StreamingResponse(generate_frames(db), media_type="multipart/x-mixed-replace; boundary=frame")

@app.post("/toggle-camera")
def toggle_camera(status: bool):
    global camera_active
    camera_active = status
    return {"camera_active": camera_active}

@app.get("/start-attendance")
def run_attendance_interface(db: Session = Depends(get_db)):
    """
    Launches a dedicated CV2 window for real-time recognition.
    Optimized for performance.
    """
    from face_detection import detect_faces
    from face_recognition import recognize_face
    import time
    
    camera = cv2.VideoCapture(0)
    # Optimization: Set lower resolution for faster processing
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("Attendance monitoring started... (Press 'Q' to stop)")

    # Prefetch students map to resolve names locally
    student_map = {s.id: s.name for s in db.query(models.Student).all()}
    
    # Track last marked time to prevent DB hammering
    last_mark_time = {}

    while True:
        ret, frame = camera.read()
        if not ret:
             break
        
        # Detect faces
        frame, detections, gray_frame = detect_faces(frame)
        
        current_time = time.time()

        for (x, y, w, h) in detections:
            # Recognize faces
            student_id, confidence = recognize_face(gray_frame, (x, y, w, h))

            if student_id != "Unknown":
                name = student_map.get(student_id, f"ID: {student_id}")
                
                # Optimization: Only hit the DB once every 30 seconds for the same person
                if student_id not in last_mark_time or (current_time - last_mark_time[student_id] > 30):
                    status_msg = mark_attendance(db, student_id)
                    last_mark_time[student_id] = current_time
                    print(f"Update: {status_msg}")
                
                # Show name and status on frame
                cv2.putText(frame, f"{name}: {confidence}%", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

        cv2.imshow('Classroom Attendance Simulation', frame)

        # Optimization: Lower waitKey for more responsive UI
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
    return {"message": "Attendance interface closed."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
