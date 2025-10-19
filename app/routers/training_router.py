from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.training_service import TrainingService
from app.schemas import TrainingCreate, TrainingOut, TrainingUpdate

router = APIRouter(
    prefix="/trainings",
    tags=["Trainings"]
)

@router.post("/", response_model=TrainingOut)
def create_training(training_data: TrainingCreate, db: Session = Depends(get_db)):
    service = TrainingService(db)
    try:
        return service.create_training(training_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=list[TrainingOut])
def get_all_trainings(db: Session = Depends(get_db)):
    service = TrainingService(db)
    return service.get_all_trainings()

@router.get("/search/name/{name}", response_model=list[TrainingOut])
def get_trainings_by_name(name: str, db: Session = Depends(get_db)):
    service = TrainingService(db)
    return service.get_trainings_by_name(name)

@router.get("/search/type/{training_type}", response_model=list[TrainingOut])
def get_trainings_by_type(training_type: str, db: Session = Depends(get_db)):
    service = TrainingService(db)
    return service.get_trainings_by_type(training_type)

@router.get("/{training_id}", response_model=TrainingOut)
def get_training(training_id: int, db: Session = Depends(get_db)):
    service = TrainingService(db)
    try:
        return service.get_training_by_id(training_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{training_id}", response_model=TrainingOut)
def update_training(training_id: int, training_update: TrainingUpdate, db: Session = Depends(get_db)):
    service = TrainingService(db)
    try:
        return service.update_training(training_id, training_update)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{training_id}")
def delete_training(training_id: int, db: Session = Depends(get_db)):
    service = TrainingService(db)
    try:
        service.delete_training(training_id)
        return {"detail": "Trening uspešno obrisan"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
