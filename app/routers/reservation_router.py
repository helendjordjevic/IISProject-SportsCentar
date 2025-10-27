from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.reservation_service import ReservationService
from app.schemas import ReservationCreate, ReservationOut, ReservationToMark
from app.services.reservation_service import get_reservations_to_mark
from fastapi import HTTPException
from typing import List

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post("/", response_model=ReservationOut)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    return ReservationService(db).create_reservation(reservation)

@router.put("/{reservation_id}/cancel", response_model=ReservationOut)
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    return ReservationService(db).cancel_reservation(reservation_id)

@router.get("/client/{client_id}", response_model=list[ReservationOut])
def get_reservations_for_client(client_id: int, db: Session = Depends(get_db)):
    return ReservationService(db).get_reservations_for_client(client_id)

@router.get("/session/{session_id}/to_mark", response_model=List[ReservationToMark])
def list_reservations_to_mark(session_id: int, db: Session = Depends(get_db)):
    return get_reservations_to_mark(db, session_id)