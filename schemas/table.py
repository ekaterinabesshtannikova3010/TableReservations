from pydantic import BaseModel

class TableCreate(BaseModel):
    name: str
    seats: int
    location: str

class Table(TableCreate):
    id: int

    class Config:
        orm_mode = True
