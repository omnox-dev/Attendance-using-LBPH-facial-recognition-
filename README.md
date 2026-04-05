# Intelligent Attendance System Using Face Recognition

## Installation Instructions

### 1. Prerequisites
- Python 3.9 or higher
- Node.js (v18+)
- A laptop with a working webcam

### 2. Backend Setup
1. Open a terminal in the `backend/` directory.
2. Install the required Python packages:
   ```bash
   pip install opencv-python opencv-contrib-python numpy pandas fastapi uvicorn sqlalchemy sqlalchemy-stubs pillow
   ```
3. Run the backend server:
   ```bash
   python main.py
   ```
   The backend will run on `http://localhost:8000`.

### 3. Frontend Setup
1. Open a terminal in the `frontend/` directory.
2. Install the Node.js packages:
   ```bash
   npm install
   ```
3. Run the Next.js development server:
   ```bash
   npm run dev
   ```
   The frontend will run on `http://localhost:3000`.

---

## Operating the System

### Step 1: Student Registration
- Go to the **Students** page on the frontend dashboard.
- Enter the Student's Name and Roll Number.
- Click **Register & Capture**.
- A webcam window will open. Stay still until 30 images are captured. The window will close automatically.

### Step 2: Training the Model
- Go to the **Dashboard** (Home page).
- Click the **Train Face Model** card.
- Wait for the success alert. This builds the face recognition model from your captured photos.

### Step 3: Start Real-Time Attendance
- Go to the **Start Attendance** page.
- Click the **Start Camera Monitoring** button.
- A webcam window will open. Position yourself in front of it.
- When the system recognizes your face, it will highlight your face in green and mark your attendance in the database.
- Press **'Q'** on your keyboard to close the camera when done.

### Step 4: Reports & Export
- Go to the **Reports** page.
- You can view the real-time attendance list.
- Click **Download CSV Report** to export all attendance records.
