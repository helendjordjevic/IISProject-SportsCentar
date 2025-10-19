from sqlalchemy.orm import Session
from app import models, schemas

class AttendanceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, attendance_id: int):
        return self.db.query(models.Attendance).filter(models.Attendance.attendance_id == attendance_id).first()

    def get_all(self):
        return self.db.query(models.Attendance).all()

    def create(self, attendance: schemas.AttendanceCreate):
        db_attendance = models.Attendance(
            client_id=attendance.client_id,
            session_id=attendance.session_id,
            attendance_date=attendance.attendance_date,
            training_rating=attendance.training_rating,
            attendance_status=attendance.attendance_status
        )
        self.db.add(db_attendance)
        self.db.commit()
        self.db.refresh(db_attendance)
        return db_attendance

    def update(self, db_attendance: models.Attendance, attendance_update: schemas.AttendanceBase):
        for field, value in attendance_update.dict(exclude_unset=True).items():
            setattr(db_attendance, field, value)
        self.db.commit()
        self.db.refresh(db_attendance)
        return db_attendance

    def delete(self, db_attendance: models.Attendance):
        self.db.delete(db_attendance)
        self.db.commit()
        return True
