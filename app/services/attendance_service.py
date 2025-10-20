from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas
from app.repositories.attendance_repository import AttendanceRepository
from typing import Optional

class AttendanceService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AttendanceRepository(db)

    def create_attendance(self, attendance_data: schemas.AttendanceCreate):
        # Proveri klijenta
        client = self.db.query(models.User).filter(models.User.user_id == attendance_data.client_id).first()
        if not client or client.user_type != models.UserTypeEnum.CLIENT:
            raise HTTPException(status_code=400, detail="Invalid client")

        # Proveri session
        session = self.db.query(models.Session).filter(models.Session.session_id == attendance_data.session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Proveri rezervaciju
        reservation = self.db.query(models.Reservation).filter(
            models.Reservation.client_id == attendance_data.client_id,
            models.Reservation.session_id == attendance_data.session_id
        ).first()

        if not reservation:
            raise HTTPException(status_code=400, detail="Client did not reserve this session")
        if reservation.status == models.ReservationStatusEnum.CANCELLED:
            raise HTTPException(status_code=400, detail="Reservation was cancelled, cannot mark attendance")

        # Proveri da li attendance već postoji
        existing_attendance = self.repo.get_by_client_and_session(attendance_data.client_id, attendance_data.session_id)
        if existing_attendance:
            raise HTTPException(status_code=400, detail="Attendance already recorded for this session")

        # Datum prisustva = datum termina
        attendance_data.attendance_date = session.start_time.date()
        # Status prisustva default na ATTENDED
        if not attendance_data.attendance_status:
            attendance_data.attendance_status = models.AttendanceStatusEnum.ATTENDED

        return self.repo.create(attendance_data)

    def update_attendance(self, attendance_id: int, attendance_update: schemas.AttendanceUpdate):
        db_att = self.repo.get_by_id(attendance_id)
        if not db_att:
            raise HTTPException(status_code=404, detail="Attendance not found")

        # Ne može se dodati ocena ako nije prisustvovao
        if attendance_update.training_rating is not None and db_att.attendance_status != models.AttendanceStatusEnum.ATTENDED:
            raise HTTPException(status_code=400, detail="Cannot rate a session you did not attend")

        # Ne može se menjati ocena ako je već postavljena
        if db_att.training_rating is not None and attendance_update.training_rating is not None:
            raise HTTPException(status_code=400, detail="Rating already given, cannot update")

        return self.repo.update(db_att, attendance_update)

    def get_attendance_by_id(self, attendance_id: int):
        db_att = self.repo.get_by_id(attendance_id)
        if not db_att:
            raise HTTPException(status_code=404, detail="Attendance not found")
        return db_att

    def get_all_attendances(self):
        return self.repo.get_all()
    
    def get_all_for_client(self, client_id: int, status: Optional[models.AttendanceStatusEnum] = None):
        return self.repo.get_all_for_client(client_id, status)
