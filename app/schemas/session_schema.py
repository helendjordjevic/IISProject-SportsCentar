from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SessionBase(BaseModel):
    start_time: datetime
    end_time: datetime
    training_id: int
    training_studio_id: Optional[int]

class SessionCreate(SessionBase):
    pass

class SessionOut(SessionBase):
    session_id: int

    class Config:
        from_attributes = True
