from sqlalchemy.orm import Session
from app import models, schemas

class TrainingStudioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, studio_id: int):
        return self.db.query(models.TrainingStudio).filter(models.TrainingStudio.training_studio_id == studio_id).first()

    def get_all(self):
        return self.db.query(models.TrainingStudio).all()

    def create(self, studio: schemas.TrainingStudioCreate):
        db_studio = models.TrainingStudio(
            training_studio_number=studio.training_studio_number,
            capacity=studio.capacity
        )
        self.db.add(db_studio)
        self.db.commit()
        self.db.refresh(db_studio)
        return db_studio

    def update(self, db_studio: models.TrainingStudio, studio_update: schemas.TrainingStudioBase):
        db_studio.training_studio_number = studio_update.training_studio_number
        db_studio.capacity = studio_update.capacity
        self.db.commit()
        self.db.refresh(db_studio)
        return db_studio

    def delete(self, db_studio: models.TrainingStudio):
        self.db.delete(db_studio)
        self.db.commit()
        return True
