from pydantic import BaseModel
from typing import Optional

class TrainingBase(BaseModel):
    name: str
    training_type: Optional[str]
    difficulty_level: Optional[str] 

class TrainingCreate(TrainingBase):
    instructor_id: int

class TrainingUpdate(BaseModel):
    name: Optional[str] = None
    training_type: Optional[str] = None
    instructor_id: Optional[int] = None
    difficulty_level: Optional[str] = None

class TrainingOut(TrainingBase):
    training_id: int
    instructor_id: int

    class Config:
        from_attributes = True
