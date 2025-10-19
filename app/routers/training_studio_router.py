from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.training_studio_service import TrainingStudioService
from app.schemas import TrainingStudioOut

router = APIRouter(
    prefix="/studios",
    tags=["Training Studios"]
)

@router.get("/", response_model=list[TrainingStudioOut])
def get_all_studios(capacity: Optional[int] = None, db: Session = Depends(get_db)):
    service = TrainingStudioService(db)
    studios = service.get_all_studios()
    
    if capacity is not None:
        # filtriramo studije po kapacitetu
        studios = [s for s in studios if s.capacity == capacity]
    
    return studios

@router.get("/{studio_number}", response_model=TrainingStudioOut)
def get_studio(studio_number: str, db: Session = Depends(get_db)):
    service = TrainingStudioService(db)
    try:
        return service.get_studio_by_number(studio_number)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
