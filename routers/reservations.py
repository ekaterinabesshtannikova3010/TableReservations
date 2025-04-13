from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.reservation_service import create_reservation, get_reservations, delete_reservation
from schemas.reservation import ReservationCreate, Reservation
from database import get_db

router = APIRouter()

@router.post("/", response_model=Reservation)
def create_new_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    return create_reservation(db=db, reservation=reservation)

@router.get("/", response_model=list[Reservation])
def read_reservations(db: Session = Depends(get_db)):
    return get_reservations(db=db)

@router.delete("/{reservation_id}", response_model=Reservation)
def remove_reservation(reservation_id: int, db: Session = Depends(get_db)):
    return delete_reservation(db=db, reservation_id=reservation_id)
