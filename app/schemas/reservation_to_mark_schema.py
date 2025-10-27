from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models import AttendanceStatusEnum

class ReservationToMark(BaseModel):
    attendance_id: Optional[int]
    client_id: int
    client_name: str
    session_id: int
    session_start_time: datetime
    session_end_time: Optional[datetime]
    attendance_marked: bool
    attendance_status: Optional[AttendanceStatusEnum]
    training_name: Optional[str]
    training_rating: Optional[int]