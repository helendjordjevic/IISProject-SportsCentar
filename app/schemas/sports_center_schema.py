from pydantic import BaseModel

class SportsCenterBase(BaseModel):
    name: str

class SportsCenterCreate(SportsCenterBase):
    pass

class SportsCenterOut(SportsCenterBase):
    sports_center_id: int

    class Config:
        from_attributes = True