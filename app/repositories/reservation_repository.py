from sqlalchemy.orm import Session
from app import models, schemas

class ReservationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, reservation_id: int):
        return self.db.query(models.Reservation).filter(models.Reservation.reservation_id == reservation_id).first()

    def get_all(self):
        return self.db.query(models.Reservation).all()

    def create(self, reservation: schemas.ReservationCreate):
        db_reservation = models.Reservation(
            client_id=reservation.client_id,
            session_id=reservation.session_id,
            reservation_date=reservation.reservation_date,
            status=reservation.status
        )
        self.db.add(db_reservation)
        self.db.commit()
        self.db.refresh(db_reservation)
        return db_reservation

    def update(self, db_reservation: models.Reservation, reservation_update: schemas.ReservationBase):
        db_reservation.status = reservation_update.status
        db_reservation.reservation_date = reservation_update.reservation_date
        self.db.commit()
        self.db.refresh(db_reservation)
        return db_reservation

    def delete(self, db_reservation: models.Reservation):
        self.db.delete(db_reservation)
        self.db.commit()
        return True
