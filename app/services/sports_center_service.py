from sqlalchemy.orm import Session
from app.repositories.sports_center_repository import SportsCenterRepository
from app import models, schemas


class SportsCenterService:
    def __init__(self, db: Session):
        self.repo = SportsCenterRepository(db)


    def get_sports_center_by_id(self, sports_center_id: int) -> schemas.TrainingOut:
        sports_center = self.repo.get_by_id(sports_center_id)
        if not sports_center:
            raise ValueError("Sports centar nije pronađen.")
        return sports_center

    def get_all_sports_centers(self):
        return self.repo.get_all()

    def get_sports_centers_by_name(self, name: str):
        return self.repo.get_by_name(name)

   
    def delete_sports_center(self, sports_center_id: int) -> bool:
        db_sports_center = self.repo.get_by_id(sports_center_id)
        if not db_sports_center:
            raise ValueError("Sports_center nije pronađen.")
        return self.repo.delete(db_sports_center)
