from sqlalchemy.orm import Session
from app import models, schemas

class TrainingStudioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_studio_number(self, studio_number: int):
        return self.db.query(models.TrainingStudio).filter(models.TrainingStudio.training_studio_number == studio_number).first()

    def get_all(self):
        return self.db.query(models.TrainingStudio).all()

  
