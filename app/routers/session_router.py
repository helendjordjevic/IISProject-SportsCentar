from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.session_service import SessionService
from app.schemas import SessionCreate, SessionOut, SessionUpdate

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)

@router.post("/", response_model=SessionOut)
def create_session(session_data: SessionCreate, db: Session = Depends(get_db)):
    service = SessionService(db)
    return service.create_session(session_data)

@router.get("/", response_model=list[SessionOut])
def get_all_sessions(db: Session = Depends(get_db)):
    service = SessionService(db)
    return service.get_all_sessions()

@router.get("/{session_id}", response_model=SessionOut)
def get_session(session_id: int, db: Session = Depends(get_db)):
    service = SessionService(db)
    return service.get_session_by_id(session_id)

@router.get("/training/{training_id}", response_model=list[SessionOut])
def get_sessions_for_training(training_id: int, db: Session = Depends(get_db)):
    service = SessionService(db)
    sessions = service.get_sessions_by_training(training_id)
    return sessions

@router.put("/{session_id}", response_model=SessionOut)
def update_session(session_id: int, session_update: SessionUpdate, db: Session = Depends(get_db)):
    service = SessionService(db)
    return service.update_session(session_id, session_update)

@router.delete("/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    service = SessionService(db)
    service.delete_session(session_id)
    return {"detail": "Session successfully deleted"}
