# Project Plan: Intelligent Attendance System Using Face Recognition

## Overview
A simple, stable, local academic project for automated attendance using face recognition.

## Technology Stack
- **Backend/AI:** Python, OpenCV, NumPy, Pandas, FastAPI
- **Face Recognition:** Haar Cascade (Detection), LBPH (Recognition)
- **Frontend:** Next.js, TailwindCSS
- **Database:** SQLite

## Project Structure
- `attendance-system/`
    - `backend/`
        - `main.py` (FastAPI entry point)
        - `face_detection.py` (Haar Cascade logic)
        - `face_recognition.py` (LBPH recognition logic)
        - `register_student.py` (Image capture & database storage)
        - `train_model.py` (LBPH trainer)
        - `attendance_service.py` (Attendance marking logic)
        - `database.py` (SQLAlchemy/SQLite setup)
        - `models.py` (Database models)
        - `haarcascade_frontalface_default.xml` (Pre-trained detection model)
        - `dataset/` (Captured student images)
        - `trainer/` (Stored `trainer.yml`)
    - `frontend/` (Next.js application)
    - `database/` (SQLite DB file)

## Implementation Phases
1. **Phase 1: Backend Architecture & Database**
   - Define SQLite schema (`students`, `attendance`).
   - Setup FastAPI boiler plate.
2. **Phase 2: Face Recognition Modules**
   - Implement Image collection for registration.
   - Implement LBPH training script.
   - Implement Real-time recognition and attendance logic.
3. **Phase 3: Frontend Development**
   - Dashboard for student management.
   - Attendance page with webcam feed (simulated or via API).
   - CSV export for reports.
4. **Phase 4: Integration & Testing**
   - Connect Frontend to Backend APIs.
   - End-to-end testing of registration -> training -> recognition.
