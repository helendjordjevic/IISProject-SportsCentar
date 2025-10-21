from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WeeklySessionReportItem(BaseModel):
    session_id: int
    training_name: str
    training_type: Optional[str]
    instructor_name: str
    training_studio_number: str
    session_start_time: datetime
    session_end_time: datetime
    attended_count: int
    average_rating: Optional[float]

    class Config:
        from_attributes = True
