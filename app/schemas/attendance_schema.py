from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from app.models import AttendanceStatusEnum

class AttendanceBase(BaseModel):
    client_id: int
    session_id: int
    attendance_date: Optional[date] = None
    training_rating: Optional[int] = Field(default=None, ge=1, le=10)
    attendance_status: AttendanceStatusEnum = AttendanceStatusEnum.ATTENDED

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    attendance_date: Optional[date] = None
    training_rating: Optional[int] = Field(default=None, ge=1, le=10)  
    attendance_status: Optional[AttendanceStatusEnum] = None

class AttendanceOut(BaseModel):
    attendance_id: int
    client_id: int
    session_id: int
    training_name: Optional[str]
    session_start_time: datetime
    session_end_time: datetime
    attendance_date: date
    attendance_status: AttendanceStatusEnum
    training_rating: Optional[int]

    class Config:
        from_attributes = True
