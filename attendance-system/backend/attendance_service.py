from sqlalchemy.orm import Session
from models import Student, Attendance
from datetime import date, datetime
import csv
import io

def mark_attendance(db: Session, student_id: int):
    """
    Records attendance in SQLite db if not already recorded today.
    Returns status message.
    """
    today = date.today()
    existing = db.query(Attendance).filter(Attendance.student_id == student_id, Attendance.date == today).first()
    
    if existing:
        return f"Attendance already marked today for Student ID: {student_id}"

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return f"Unknown Student ID: {student_id}"

    new_attendance = Attendance(
        student_id=student_id,
        date=today,
        time=datetime.now().time(),
        status="Present"
    )
    db.add(new_attendance)
    db.commit()
    return f"Welcome {student.name} – Attendance Marked"

def get_today_attendance():
    """ Returns attendance log for current day from DB """
    # Placeholder - implementation would use DB session
    pass

def export_attendance_csv(db: Session):
    """ Generates CSV payload for attendance records """
    records = db.query(Attendance).join(Student).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Roll Number', 'Date', 'Time', 'Status'])
    
    for record in records:
        writer.writerow([
            record.id, 
            record.student.name, 
            record.student.roll_number, 
            record.date, 
            record.time, 
            record.status
        ])
        
    return output.getvalue()
