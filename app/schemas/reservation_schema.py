from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.models import ReservationStatusEnum

class ReservationBase(BaseModel):
    client_id: int
    session_id: int
    reservation_date: date
    status: ReservationStatusEnum

class ReservationCreate(ReservationBase):
    client_id: int
    session_id: int
    reservation_date: date
    status: Optional[ReservationStatusEnum] = None 

class ReservationUpdate(BaseModel):
    status: Optional[ReservationStatusEnum] = None

class ReservationOut(ReservationBase):
    reservation_id: int

    class Config:
        from_attributes = True
