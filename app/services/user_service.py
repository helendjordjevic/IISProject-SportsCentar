from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate, UserUpdate, UserOut
from app.utils.security import  verify_password
from app.models import User


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self, user_data: UserCreate) -> UserOut:
        existing = self.repo.get_by_email(user_data.email)
        if existing:
            raise ValueError("Korisnik sa ovom email adresom već postoji.")

        new_user = self.repo.create(user_data)
        return new_user

    def get_user_by_id(self, user_id: int) -> UserOut | None:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("Korisnik nije pronađen.")
        return user

    def get_user_by_email(self, email: str) -> UserOut | None:
        user = self.repo.get_by_email(email)
        if not user:
            raise ValueError("Korisnik nije pronađen.")
        return user

    def get_all_users(self):
        return self.repo.get_all()

    def update_user(self, user_id: int, user_update: UserUpdate) -> UserOut:
        db_user = self.repo.get_by_id(user_id)
        if not db_user:
            raise ValueError("Korisnik nije pronađen.")
        updated_user = self.repo.update(db_user, user_update)
        return updated_user

    def delete_user(self, user_id: int) -> bool:
        db_user = self.repo.get_by_id(user_id)
        if not db_user:
            raise ValueError("Korisnik nije pronađen.")
        return self.repo.delete(db_user)

    def authenticate_user(self, email: str, password: str) -> User | None:
        """Proverava da li korisnik postoji i da li mu se lozinka poklapa."""
        user = self.repo.get_by_email(email)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user
