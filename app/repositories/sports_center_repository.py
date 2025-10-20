from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import models, schemas

class SportsCenterRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, sc: schemas.SportsCenterCreate):
        db_sc = models.SportsCenter(name=sc.name)
        self.db.add(db_sc)
        self.db.commit()
        self.db.refresh(db_sc)
        return db_sc

    def get_by_id(self, sc_id: int):
        return self.db.query(models.SportsCenter).filter(models.SportsCenter.sports_center_id == sc_id).first()

    def get_all(self):
        return self.db.query(models.SportsCenter).all()

    def get_by_name(self, name: str):
        # case-insensitive partial match
        return self.db.query(models.SportsCenter).filter(models.SportsCenter.name.ilike(f"%{name}%")).all()

    def delete(self, sc: models.SportsCenter):
        self.db.delete(sc)
        self.db.commit()
        return True
