from pydantic import BaseModel
from typing import Optional

class TrainingBase(BaseModel):
    name: str
    training_type: Optional[str]

class TrainingCreate(TrainingBase):
    instructor_id: int

class TrainingOut(TrainingBase):
    training_id: int
    instructor_id: int

    class Config:
        from_attributes = True
