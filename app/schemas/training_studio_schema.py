from pydantic import BaseModel

class TrainingStudioBase(BaseModel):
    training_studio_number: str
    capacity: int

class TrainingStudioCreate(TrainingStudioBase):
    pass

class TrainingStudioOut(TrainingStudioBase):
    training_studio_id: int

    class Config:
        from_attributes = True
