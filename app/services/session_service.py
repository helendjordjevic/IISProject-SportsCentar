from sqlalchemy.orm import Session
from app.repositories.session_repository import SessionRepository
from app.repositories.training_repository import TrainingRepository
from app import models, schemas
from fastapi import HTTPException, status

class SessionService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = SessionRepository(db)
        self.training_repo = TrainingRepository(db)
        
    def create_session(self, session_data: schemas.SessionCreate):
        training = self.training_repo.get_by_id(session_data.training_id)
        if not training:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training not found")

        # 🔍 Proveri zauzetost studija
        overlapping_studio = self.db.query(models.Session).filter(
            models.Session.training_studio_id == session_data.training_studio_id,
            models.Session.start_time < session_data.end_time,
            models.Session.end_time > session_data.start_time
        ).first()

        if overlapping_studio:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Studio already has a session scheduled during that time"
            )

        # 🔍 Proveri zauzetost instruktora
        overlapping_instructor = (
            self.db.query(models.Session)
            .join(models.Training)
            .filter(
                models.Training.instructor_id == training.instructor_id,
                models.Session.start_time < session_data.end_time,
                models.Session.end_time > session_data.start_time
            )
            .first()
        )

        if overlapping_instructor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Instructor already has another session at that time"
            )

        return self.repository.create(session_data)

    def get_session_by_id(self, session_id: int):
        session = self.repository.get_by_id(session_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        return session

    def get_all_sessions(self):
        return self.repository.get_all()
    
    def get_sessions_by_training(self, training_id: int):
        return self.repository.get_by_training_id(training_id)

    def update_session(self, session_id: int, session_update: schemas.SessionUpdate):
        db_session = self.repository.get_by_id(session_id)
        if not db_session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

        # Ako se ažurira training_id, proveri novog trenera
        training_id = session_update.training_id or db_session.training_id
        training = self.training_repo.get_by_id(training_id)
        if not training:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training not found")

        # 🔍 Provera zauzetosti studija (bez trenutnog termina)
        overlapping_studio = self.db.query(models.Session).filter(
            models.Session.training_studio_id == (session_update.training_studio_id or db_session.training_studio_id),
            models.Session.session_id != session_id,
            models.Session.start_time < (session_update.end_time or db_session.end_time),
            models.Session.end_time > (session_update.start_time or db_session.start_time)
        ).first()

        if overlapping_studio:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Studio already has another session during that time"
            )

        # 🔍 Proveri zauzetost instruktora
        overlapping_instructor = (
            self.db.query(models.Session)
            .join(models.Training)
            .filter(
                models.Training.instructor_id == training.instructor_id,
                models.Session.session_id != session_id,
                models.Session.start_time < (session_update.end_time or db_session.end_time),
                models.Session.end_time > (session_update.start_time or db_session.start_time)
            )
            .first()
        )

        if overlapping_instructor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Instructor already has another session at that time"
            )

        return self.repository.update(db_session, session_update)

    def delete_session(self, session_id: int):
        db_session = self.repository.get_by_id(session_id)
        if not db_session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        return self.repository.delete(db_session)
