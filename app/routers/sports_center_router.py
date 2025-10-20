from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.sports_center_service import SportsCenterService
from app.schemas import SportsCenterCreate, SportsCenterOut

router = APIRouter(
    prefix="/sports_centers",
    tags=["Sports Centers"]
)


@router.get("/", response_model=list[SportsCenterOut])
def get_all_sports_center(db: Session = Depends(get_db)):
    service = SportsCenterService(db)
    return service.get_all_sports_centers()

@router.get("/search/name/{name}", response_model=list[SportsCenterOut])
def get_sports_center_by_name(name: str, db: Session = Depends(get_db)):
    service = SportsCenterService(db)
    return service.get_sports_centers_by_name(name)

@router.get("/{sports_center_id}", response_model=SportsCenterOut)
def get_sports_centers_by_id(sports_center_id: int, db: Session = Depends(get_db)):
    service = SportsCenterService(db)
    try:
        return service.get_sports_center_by_id(sports_center_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{sports_center_id}")
def delete_sports_centers(sports_center_id: int, db: Session = Depends(get_db)):
    service = SportsCenterService(db)
    try:
        service.delete_sports_center(sports_center_id)
        return {"detail": "Sport centar uspešno obrisan"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
