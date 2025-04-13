from sqlalchemy.orm import Session
from models.table import Table
from schemas.table import TableCreate

def create_table(db: Session, table: TableCreate):
    db_table = Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

def get_tables(db: Session):
    return db.query(Table).all()

def delete_table(db: Session, table_id: int):
    db_table = db.query(Table).filter(Table.id == table_id).first()
    if db_table:
        db.delete(db_table)
        db.commit()
    return db_table
