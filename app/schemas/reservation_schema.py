from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from app.models import ReservationStatusEnum

class ReservationBase(BaseModel):
    client_id: int
    session_id: int
    reservation_date: date
    status: ReservationStatusEnum = None

class ReservationCreate(ReservationBase):
    status: Optional[ReservationStatusEnum] = None 

class ReservationUpdate(BaseModel):
    status: Optional[ReservationStatusEnum] = None

class ReservationOut(BaseModel):
    reservation_id: int
    client_id: int
    session_id: int
    reservation_date: date
    status: ReservationStatusEnum
    training_name: str
    session_start_time: datetime
    session_end_time: datetime


    class Config:
        from_orm = True
