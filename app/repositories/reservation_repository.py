from sqlalchemy.orm import Session
from app import models, schemas

class ReservationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, reservation_id: int):
        return self.db.query(models.Reservation).filter(models.Reservation.reservation_id == reservation_id).first()

    def get_all(self):
        return self.db.query(models.Reservation).all()

    def get_all_for_client(self, client_id: int):
        return self.db.query(models.Reservation).filter(models.Reservation.client_id == client_id).all()

    def count_active_for_session(self, session_id: int):
        return self.db.query(models.Reservation).filter(
            models.Reservation.session_id == session_id,
            models.Reservation.status == models.ReservationStatusEnum.RESERVED
        ).count()

    def create(self, reservation: schemas.ReservationCreate):
        db_res = models.Reservation(
            client_id=reservation.client_id,
            session_id=reservation.session_id,
            reservation_date=reservation.reservation_date,
            status=reservation.status
        )
        self.db.add(db_res)
        self.db.commit()
        self.db.refresh(db_res)
        return db_res

