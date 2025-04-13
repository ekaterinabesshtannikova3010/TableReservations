from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.table_service import create_table, get_tables, delete_table
from schemas.table import TableCreate, Table
from database import get_db

router = APIRouter()

@router.post("/", response_model=Table)
def create_new_table(table: TableCreate, db: Session = Depends(get_db)):
    return create_table(db=db, table=table)

@router.get("/", response_model=list[Table])
def read_tables(db: Session = Depends(get_db)):
    return get_tables(db=db)

@router.delete("/{table_id}", response_model=Table)
def remove_table(table_id: int, db: Session = Depends(get_db)):
    return delete_table(db=db, table_id=table_id)
