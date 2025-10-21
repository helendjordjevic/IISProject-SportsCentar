from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app import models, schemas
from app.repositories.reservation_repository import ReservationRepository

class ReservationService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ReservationRepository(db)

    def create_reservation(self, reservation_data: schemas.ReservationCreate):
        # 🔹 1. Proveri klijenta
        client = self.db.query(models.User).filter(models.User.user_id == reservation_data.client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        if client.user_type != models.UserTypeEnum.CLIENT:
            raise HTTPException(status_code=400, detail="Only clients can make reservations")

        # 🔹 2. Proveri termin
        session = self.db.query(models.Session).filter(models.Session.session_id == reservation_data.session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # 🔹 3. Da li već postoji rezervacija
        existing = self.db.query(models.Reservation).filter(
            models.Reservation.client_id == reservation_data.client_id,
            models.Reservation.session_id == reservation_data.session_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="You already have a reservation for this session")

        # 🔹 4. Da li ima mesta
        capacity = session.training_studio.capacity if session.training_studio else 0
        active_reservations = self.repo.count_active_for_session(session.session_id)

        if active_reservations >= capacity:
            raise HTTPException(status_code=400, detail="Session is full")

        # 🔹 5. Kreiraj rezervaciju
        reservation_data.status = models.ReservationStatusEnum.RESERVED
        return self.repo.create(reservation_data)

    def cancel_reservation(self, reservation_id: int):
        db_res = self.repo.get_by_id(reservation_id)
        if not db_res:
            raise HTTPException(status_code=404, detail="Reservation not found")

        db_res.status = models.ReservationStatusEnum.CANCELLED
        self.db.commit()
        self.db.refresh(db_res)

        # Formiraj response dict
        return {
            "reservation_id": db_res.reservation_id,
            "client_id": db_res.client_id,
            "session_id": db_res.session.session_id,
            "training_name": db_res.session.training.name,
            "session_start_time": db_res.session.start_time,
            "session_end_time": db_res.session.end_time,
            "reservation_date": db_res.reservation_date,
            "status": db_res.status.value
        }

    
    def get_reservation_by_id(self, reservation_id: int):
        db_res = self.repo.get_by_id(reservation_id)
        if not db_res:
            raise HTTPException(status_code=404, detail="Reservation not found")
        return db_res


    def get_reservations_for_client(self, client_id: int):
        client = self.db.query(models.User).filter(models.User.user_id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")

        reservations = (
            self.db.query(models.Reservation)
            .filter(models.Reservation.client_id == client_id)
            .options(
                joinedload(models.Reservation.session).joinedload(models.Session.training)
            )
            .all()
        )

        result = []
        for r in reservations:
            result.append({
                "reservation_id": r.reservation_id,
                "client_id": r.client_id,
                "session_id": r.session.session_id,
                "training_name": r.session.training.name,
                "session_start_time": r.session.start_time,
                "session_end_time": r.session.end_time,
                "reservation_date": r.reservation_date,
                "status": r.status.value  # ako je Enum
            })
        return result
