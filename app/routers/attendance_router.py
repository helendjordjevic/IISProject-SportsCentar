from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.attendance_service import AttendanceService
from app.schemas import AttendanceCreate, AttendanceUpdate, AttendanceOut
from app.schemas import WeeklySessionReportItem
from app.models import AttendanceStatusEnum
from typing import Optional, List
from datetime import datetime

# PDF generation imports
from fastapi.responses import StreamingResponse
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from fastapi import HTTPException


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


@router.get("/reports/weekly/pdf")
def download_weekly_report_pdf(
    week_start_date: datetime = Query(..., description="Datum početka sedmice (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    service = AttendanceService(db)
    report_items = service.get_weekly_report(week_start_date)

    # ako slučajno get_weekly_report vraća tuple (report, nešto), uzmi samo prvi deo
    if isinstance(report_items, tuple):
        report_items = report_items[0]

    if not report_items:
        raise HTTPException(status_code=404, detail="No sessions found for this week")

    # Priprema PDF-a u memoriji
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    # Naslov
    elements = [Paragraph(f"Weekly Training Report — {week_start_date.strftime('%Y-%m-%d')}", styles["Title"])]

    # Header + redovi
    table_data = [
        ["Session ID", "Training", "Instructor", "Studio", "Start", "End", "Attended", "Avg Rating"]
    ]

    for item in report_items:
        table_data.append([
            item.session_id,
            item.training_name,
            item.instructor_name,
            item.training_studio_number,
            item.session_start_time.strftime("%Y-%m-%d %H:%M"),
            item.session_end_time.strftime("%Y-%m-%d %H:%M"),
            item.attended_count,
            item.average_rating if item.average_rating is not None else "-"
        ])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=weekly_report_{week_start_date.strftime('%Y-%m-%d')}.pdf"
        }
    )