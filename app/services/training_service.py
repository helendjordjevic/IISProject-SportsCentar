from sqlalchemy.orm import Session
from app.repositories.training_repository import TrainingRepository
from app import models, schemas


class TrainingService:
    def __init__(self, db: Session):
        self.repo = TrainingRepository(db)

    def create_training(self, training_data: schemas.TrainingCreate) -> schemas.TrainingOut:
        # opcionalno proveri instruktor
        instructor = self.repo.db.query(models.User).filter(
            models.User.user_id == training_data.instructor_id
        ).first()
        if not instructor:
            raise ValueError("Instruktor nije pronađen.")

        return self.repo.create(training_data)

    def get_training_by_id(self, training_id: int) -> schemas.TrainingOut:
        training = self.repo.get_by_id(training_id)
        if not training:
            raise ValueError("Trening nije pronađen.")
        return training

    def get_all_trainings(self):
        return self.repo.get_all()

    def get_trainings_by_name(self, name: str):
        return self.repo.get_by_name(name)

    def get_trainings_by_type(self, training_type: str):
        return self.repo.get_by_type(training_type)

    def update_training(self, training_id: int, training_update: schemas.TrainingUpdate):
        db_training = self.repo.get_by_id(training_id)
        if not db_training:
            raise ValueError("Trening nije pronađen.")

        # Ako se menja instruktor, proverimo da li je INSTRUCTOR
        if training_update.instructor_id is not None:
            instructor = self.repo.db.query(models.User).filter(
                models.User.user_id == training_update.instructor_id,
                models.User.user_type == "INSTRUCTOR"
            ).first()
            if not instructor:
                raise ValueError("Instructor mora biti INSTRUCTOR tip korisnika.")

        return self.repo.update(db_training, training_update)
    
    def delete_training(self, training_id: int) -> bool:
        db_training = self.repo.get_by_id(training_id)
        if not db_training:
            raise ValueError("Trening nije pronađen.")
        return self.repo.delete(db_training)
