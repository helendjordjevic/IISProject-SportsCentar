from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.session_repository import SessionRepository
from app.repositories.training_repository import TrainingRepository
from app import models, schemas


class SessionService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = SessionRepository(db)
        self.training_repo = TrainingRepository(db)

    def create_session(self, session_data: schemas.SessionCreate) -> models.Session:
        training = self.training_repo.get_by_id(session_data.training_id)
        if not training:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training not found")

        self._check_conflicts(session_data)

        # Set weekday i day period pre kreiranja
        self._set_weekday_and_period(session_data)

        return self.repository.create(session_data)

    def update_session(self, session_id: int, session_update: schemas.SessionUpdate) -> models.Session:
        db_session = self.repository.get_by_id(session_id)
        if not db_session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

        # Ako se menja training_id, proveri instruktor
        training_id = session_update.training_id or db_session.training_id
        training = self.training_repo.get_by_id(training_id)
        if not training:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training not found")

        self._check_conflicts(session_update, exclude_session_id=session_id)

        # Ako se menja start_time, update weekday i day period 
        if session_update.start_time:
            self._set_weekday_and_period(session_update)

        return self.repository.update(db_session, session_update)

    def delete_session(self, session_id: int) -> bool:
        db_session = self.repository.get_by_id(session_id)
        if not db_session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        return self.repository.delete(db_session)

    def get_session_by_id(self, session_id: int) -> models.Session:
        session = self.repository.get_by_id(session_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        return session

    def get_all_sessions(self):
        return self.repository.get_all()

    def get_sessions_by_training(self, training_id: int):
        return self.repository.get_by_training_id(training_id)

    # --- Privatne metode ---

    def _check_conflicts(self, session_data, exclude_session_id: int = None):
        # Zauzetost studija
        q_studio = self.db.query(models.Session).filter(
            models.Session.training_studio_id == session_data.training_studio_id,
            models.Session.start_time < session_data.end_time,
            models.Session.end_time > session_data.start_time
        )
        if exclude_session_id:
            q_studio = q_studio.filter(models.Session.session_id != exclude_session_id)
        if q_studio.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Studio already has another session during that time")

        # Zauzetost instruktora
        q_instr = self.db.query(models.Session).join(models.Training).filter(
            models.Training.instructor_id == self.training_repo.get_by_id(session_data.training_id).instructor_id,
            models.Session.start_time < session_data.end_time,
            models.Session.end_time > session_data.start_time
        )
        if exclude_session_id:
            q_instr = q_instr.filter(models.Session.session_id != exclude_session_id)
        if q_instr.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Instructor already has another session at that time")

    def _set_weekday_and_period(self, session_data):
        # Weekday
        session_data.weekday = session_data.start_time.strftime("%A").upper()

        # day period
        hour = session_data.start_time.hour
        if hour < 12:
            session_data.day_period = "MORNING"
        elif hour < 19:
            session_data.day_period = "AFTERNOON"
        else:
            session_data.day_period = "EVENING"
