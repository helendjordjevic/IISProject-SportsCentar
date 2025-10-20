from sqlalchemy.orm import Session
from app import models, schemas

class AttendanceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, attendance_data: schemas.AttendanceCreate):
        attendance = models.Attendance(**attendance_data.dict())
        self.db.add(attendance)
        self.db.commit()
        self.db.refresh(attendance)
        return attendance

    def get_by_id(self, attendance_id: int):
        return self.db.query(models.Attendance).filter(models.Attendance.attendance_id == attendance_id).first()

    def get_all(self):
        return self.db.query(models.Attendance).all()

    def get_all_for_client(self, client_id: int, status=None):
        query = self.db.query(models.Attendance).filter(models.Attendance.client_id == client_id)
        if status:
            query = query.filter(models.Attendance.attendance_status == status)
        return query.all()

    def update(self, db_attendance, attendance_update: schemas.AttendanceUpdate):
        for key, value in attendance_update.dict(exclude_unset=True).items():
            setattr(db_attendance, key, value)
        self.db.commit()
        self.db.refresh(db_attendance)
        return db_attendance

    # ✅ Ova metoda ti je falila
    def get_by_client_and_session(self, client_id: int, session_id: int):
        return self.db.query(models.Attendance).filter(
            models.Attendance.client_id == client_id,
            models.Attendance.session_id == session_id
        ).first()
