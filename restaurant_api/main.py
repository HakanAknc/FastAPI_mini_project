# 1. Gerekli Kütüphanelerin İçe Aktarılması
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from datetime import datetime
from typing import List


# 2. Veritabanı Bağlantısı ve Modeller
# Veritabanı bağlantı bilgileri
DATABASE_URL = "postgresql://postgres:12345@127.0.0.1:5432/restaurant"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, index=True)
    email = Column(String, index=True)

class Table(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, index=True)
    seats = Column(Integer)

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    table_id = Column(Integer, ForeignKey("tables.id"))
    date_time = Column(DateTime, default=datetime.utcnow)
    customer = relationship("Customer")
    table = relationship("Table")

Base.metadata.create_all(bind=engine)

# 3. FastAPI Uygulamasını Oluşturma
app = FastAPI()

# 4. Veritabanı Bağlantısını Sağlama
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 5. Müşteri Yönetimi Endpoints
# a) Müşteri Ekleme
class CustomerCreate(BaseModel):
    name: str
    phone: str
    email: str

@app.post("/customers", response_model=CustomerCreate)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# b) Masaları Listeleme
@app.get("/customers", response_model=List[CustomerCreate])
def list_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()

# 6. Masa Yönetimi Endpoints
# a) Masa Ekleme
class TableCreate(BaseModel):
    number: int
    seats: int

@app.post("/tables", response_model=TableCreate)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    db_table = Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

# b) Masaları Listeleme
@app.get("/tables", response_model=List[TableCreate])
def list_tables(db: Session = Depends(get_db)):
    return db.query(Table).all()


# 7. Rezervasyon Yönetimi Endpoints
# a) Rezervasyon Yapma
class ReservationCreate(BaseModel):
    customer_id: int
    table_id: int
    date_time: datetime

@app.post("/reservations", response_model=ReservationCreate)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    db_reservation = Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@app.get("/reservations", response_model=List[ReservationCreate])
def list_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).all()


