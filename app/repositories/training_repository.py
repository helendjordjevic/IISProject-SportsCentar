from sqlalchemy.orm import Session
from app import models, schemas

class TrainingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, training_id: int):
        return self.db.query(models.Training).filter(models.Training.training_id == training_id).first()

    def get_all(self):
        return self.db.query(models.Training).all()

    def create(self, training: schemas.TrainingCreate):
        db_training = models.Training(
            name=training.name,
            training_type=training.training_type,
            instructor_id=training.instructor_id
        )
        self.db.add(db_training)
        self.db.commit()
        self.db.refresh(db_training)
        return db_training

    def update(self, db_training: models.Training, training_update: schemas.TrainingBase):
        db_training.name = training_update.name
        db_training.training_type = training_update.training_type
        self.db.commit()
        self.db.refresh(db_training)
        return db_training

    def delete(self, db_training: models.Training):
        self.db.delete(db_training)
        self.db.commit()
        return True
