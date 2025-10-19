from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserOut, UserUpdate
from app.schemas.user_schema import LoginRequest, LoginResponse



router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=List[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_all_users()


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.get_user_by_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/email/{email}", response_model=UserOut)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.get_user_by_email(email)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.update_user(user_id, user_update)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    return {"message": "Korisnik je uspešno izbrisan"}


@router.post("/login", response_model=LoginResponse)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.authenticate_user(login_data.email, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Neispravna email adresa ili lozinka."
        )

    return LoginResponse(
        message="Uspešna prijava!",
        user_id=user.user_id,
        email=user.email,
        user_type=user.user_type
    )