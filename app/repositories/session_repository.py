from sqlalchemy.orm import Session
from app import models, schemas

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, session_id: int):
        return self.db.query(models.Session).filter(models.Session.session_id == session_id).first()

    def get_all(self):
        return self.db.query(models.Session).all()

    def create(self, session: schemas.SessionCreate):
        db_session = models.Session(
            start_time=session.start_time,
            end_time=session.end_time,
            training_id=session.training_id,
            training_studio_id=session.training_studio_id
        )
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        return db_session

    def update(self, db_session: models.Session, session_update: schemas.SessionUpdate):
        for field, value in session_update.dict(exclude_unset=True).items():
            setattr(db_session, field, value)
        self.db.commit()
        self.db.refresh(db_session)
        return db_session

    def delete(self, db_session: models.Session):
        self.db.delete(db_session)
        self.db.commit()
        return True
