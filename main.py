from fastapi import FastAPI
from routers import tables, reservations
from database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(tables.router, prefix="/tables", tags=["tables"])
app.include_router(reservations.router, prefix="/reservations", tags=["reservations"])
