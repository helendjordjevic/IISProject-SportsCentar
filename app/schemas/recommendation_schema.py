from pydantic import BaseModel
from typing import Optional

class RecommendationOut(BaseModel):
    training_id: int
    training_name: str
    training_type: Optional[str] = None
    difficulty_level: Optional[str] = None
    instructor_name: str

    class Config:
        orm_mode = True
