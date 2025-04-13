from sqlalchemy.orm import Session
from models.reservation import Reservation
from schemas.reservation import ReservationCreate
from datetime import datetime, timedelta

def create_reservation(db: Session, reservation: ReservationCreate):
    db_reservation = Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def get_reservations(db: Session):
    return db.query(Reservation).all()

def delete_reservation(db: Session, reservation_id: int):
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation:
        db.delete(db_reservation)
        db.commit()
    return db_reservation
