from pydantic import BaseModel
from datetime import date
from app.models import ReservationStatusEnum

class ReservationBase(BaseModel):
    client_id: int
    session_id: int
    reservation_date: date
    status: ReservationStatusEnum

class ReservationCreate(ReservationBase):
    pass

class ReservationOut(ReservationBase):
    reservation_id: int

    class Config:
        from_attributes = True
