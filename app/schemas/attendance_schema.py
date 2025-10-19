from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.models import AttendanceStatusEnum

class AttendanceBase(BaseModel):
    client_id: int
    session_id: int
    attendance_date: Optional[date]
    training_rating: Optional[int]
    attendance_status: AttendanceStatusEnum

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceOut(AttendanceBase):
    attendance_id: int

    class Config:
        from_attributes = True
