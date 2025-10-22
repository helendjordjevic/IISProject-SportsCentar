from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.training_repository import TrainingRepository
from app import models, schemas


class TrainingService:
    def __init__(self, db: Session):
        self.repo = TrainingRepository(db)

    def create_training(self, training_data: schemas.TrainingCreate) -> schemas.TrainingOut:
        instructor = self.repo.db.query(models.User).filter(
            models.User.user_id == training_data.instructor_id,
            models.User.user_type == "INSTRUCTOR"
        ).first()
        if not instructor:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Instruktor nije pronađen ili nije INSTRUCTOR")

        db_training = self.repo.create(training_data)
        return schemas.TrainingOut.from_orm(db_training)

    def get_training_by_id(self, training_id: int) -> schemas.TrainingOut:
        training = self.repo.get_by_id(training_id)
        if not training:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trening nije pronađen")
        return schemas.TrainingOut.from_orm(training)

    def get_all_trainings(self):
        return [schemas.TrainingOut.from_orm(t) for t in self.repo.get_all()]

    def get_trainings_by_name(self, name: str):
        return [schemas.TrainingOut.from_orm(t) for t in self.repo.get_by_name(name)]

    def get_trainings_by_type(self, training_type: str):
        return [schemas.TrainingOut.from_orm(t) for t in self.repo.get_by_type(training_type)]

    def update_training(self, training_id: int, training_update: schemas.TrainingUpdate) -> schemas.TrainingOut:
        db_training = self.repo.get_by_id(training_id)
        if not db_training:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trening nije pronađen")

        if training_update.instructor_id is not None:
            instructor = self.repo.db.query(models.User).filter(
                models.User.user_id == training_update.instructor_id,
                models.User.user_type == "INSTRUCTOR"
            ).first()
            if not instructor:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Instruktor mora biti INSTRUCTOR tip korisnika")

        updated = self.repo.update(db_training, training_update)
        return schemas.TrainingOut.from_orm(updated)

    def delete_training(self, training_id: int) -> bool:
        db_training = self.repo.get_by_id(training_id)
        if not db_training:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trening nije pronađen")
        return self.repo.delete(db_training)
