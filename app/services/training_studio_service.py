from sqlalchemy.orm import Session
from app.repositories.training_studio_repository import TrainingStudioRepository
from app.schemas import TrainingStudioOut

class TrainingStudioService:
    def __init__(self, db: Session):
        self.repo = TrainingStudioRepository(db)

    def get_studio_by_number(self, studio_number: str) -> TrainingStudioOut:
        studio = self.repo.get_by_studio_number(studio_number)
        if not studio:
            raise ValueError("Studio nije pronađen.")
        return studio

    def get_all_studios(self):
        return self.repo.get_all()
