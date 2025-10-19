from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models import UserTypeEnum

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    user_type: UserTypeEnum

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserOut(UserBase):
    user_id: int

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    message: str
    user_id: int
    email: EmailStr
    user_type: str