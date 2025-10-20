from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SessionBase(BaseModel):
    start_time: datetime
    end_time: datetime
    training_id: int
    training_studio_id: Optional[int] = None

class SessionCreate(SessionBase):
    pass

class SessionUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    training_id: Optional[int] = None
    training_studio_id: Optional[int] = None

class SessionOut(SessionBase):
    session_id: int

    class Config:
        from_attributes = True