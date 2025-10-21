from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.attendance_service import AttendanceService
from app.schemas import AttendanceCreate, AttendanceUpdate, AttendanceOut
from app.schemas import WeeklySessionReportItem
from app.models import AttendanceStatusEnum
from typing import Optional, List
from datetime import datetime


router = APIRouter(prefix="/attendances", tags=["Attendances"])

@router.post("/", response_model=AttendanceOut)
def create_attendance(attendance_data: AttendanceCreate, db: Session = Depends(get_db)):
    service = AttendanceService(db)
    return service.create_attendance(attendance_data)

@router.put("/{attendance_id}", response_model=AttendanceOut)
def update_attendance(attendance_id: int, attendance_update: AttendanceUpdate, db: Session = Depends(get_db)):
    service = AttendanceService(db)
    return service.update_attendance(attendance_id, attendance_update)

@router.get("/", response_model=list[AttendanceOut])
def get_all_attendances(db: Session = Depends(get_db)):
    service = AttendanceService(db)
    return service.get_all_attendances()

@router.get("/client/{client_id}", response_model=list[AttendanceOut])
def get_all_for_client(
    client_id: int,
    status: Optional[AttendanceStatusEnum] = None,
    db: Session = Depends(get_db)
):
    service = AttendanceService(db)
    return service.get_all_for_client(client_id, status)

@router.get("/{attendance_id}", response_model=AttendanceOut)
def get_attendance_by_id(attendance_id: int, db: Session = Depends(get_db)):
    service = AttendanceService(db)
    return service.get_attendance_by_id(attendance_id)

@router.get("/reports/weekly", response_model=List[WeeklySessionReportItem])
def get_weekly_report(
    week_start_date: datetime = Query(..., description="Datum početka sedmice (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    service = AttendanceService(db)
    report = service.get_weekly_report(week_start_date)
    return report