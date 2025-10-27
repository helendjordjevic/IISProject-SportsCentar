from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app import models, schemas
from app.repositories.attendance_repository import AttendanceRepository
from typing import Optional
from collections import defaultdict
from datetime import datetime, timedelta


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

        if attendance_update.training_rating is not None and db_att.attendance_status != models.AttendanceStatusEnum.ATTENDED:
            raise HTTPException(status_code=400, detail="Cannot rate a session you did not attend")

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
        attendances = (
            self.db.query(models.Attendance)
            .filter(models.Attendance.client_id == client_id)
            .options(
                joinedload(models.Attendance.session).joinedload(models.Session.training)
            )
            .all()
        )

        result = []
        for a in attendances:
            if status and a.attendance_status != status:
                continue

            result.append({
                "attendance_id": a.attendance_id,
                "client_id": a.client_id,
                "session_id": a.session.session_id,
                "training_name": a.session.training.name if a.session.training else None,
                "session_start_time": a.session.start_time,
                "session_end_time": a.session.end_time,
                "attendance_date": a.attendance_date,
                "attendance_status": a.attendance_status.value,
                "training_rating": a.training_rating
            })
        return result

    def get_weekly_report(self, week_start_date: datetime):
        week_start = week_start_date
        week_end = week_start + timedelta(days=7)

        attendances = (
            self.db.query(models.Attendance)
            .join(models.Attendance.session)
            .options(
                joinedload(models.Attendance.session).joinedload(models.Session.training).joinedload(models.Training.instructor),
                joinedload(models.Attendance.session).joinedload(models.Session.training_studio)
            )
            .filter(
                models.Attendance.attendance_status == models.AttendanceStatusEnum.ATTENDED,
                models.Session.start_time >= week_start,
                models.Session.start_time <= week_end
                )
            .all()
        )

        sessions_dict = defaultdict(list)
        for attendance in attendances:
            sessions_dict[attendance.session].append(attendance)

        report = []
        for session, session_attendances in sessions_dict.items():
            attended_count = len(session_attendances)
            average_rating = (
                sum(a.training_rating for a in session_attendances if a.training_rating is not None)
                / attended_count
                if attended_count > 0 else None
            )

            report.append(schemas.WeeklySessionReportItem(
                session_id=session.session_id,
                training_name=session.training.name,
                training_type=session.training.training_type,
                instructor_name=f"{session.training.instructor.first_name} {session.training.instructor.last_name}",
                training_studio_number=session.training_studio.training_studio_number,
                session_start_time=session.start_time,
                session_end_time=session.end_time,
                attended_count=attended_count,
                average_rating=round(average_rating, 2) if average_rating else None
            ))

        # Sortiraj po start_time
        report.sort(key=lambda x: x.session_start_time)

        return report