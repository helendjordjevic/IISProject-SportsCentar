from sqlalchemy.orm import Session
from app import models, schemas
from app.utils.security import hash_password  


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int):
        return self.db.query(models.User).filter(models.User.user_id == user_id).first()

    def get_by_email(self, email: str):
        return self.db.query(models.User).filter(models.User.email == email).first()
    
    def get_all(self):
        return self.db.query(models.User).all()


    def create(self, user: schemas.UserCreate):
        hashed_password = hash_password(user.password) 
        db_user = models.User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=hashed_password,
            user_type=user.user_type
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, db_user: models.User, user_update: schemas.UserUpdate):
        for field, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, field, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, db_user: models.User):
        self.db.delete(db_user)
        self.db.commit()
        return True
