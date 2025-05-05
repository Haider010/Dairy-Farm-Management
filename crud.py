from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from contextlib import contextmanager
from typing import Generator, Any

# -----------------------------
# Database Schema Definitions:
# -----------------------------
# Animal:
#   id: Integer, Primary Key
#   name: String
#   breed: String
#   date_of_birth: Date
#   notes: String (optional)
# MilkRecord:
#   id: Integer, Primary Key
#   animal_id: Integer, Foreign Key -> Animal.id
#   date: Date
#   quantity_liters: Float
# FeedRecord:
#   id: Integer, Primary Key
#   animal_id: Integer, Foreign Key -> Animal.id
#   date: Date
#   feed_type: String
#   quantity_kg: Float
# MedicineRecord:
#   id: Integer, Primary Key
#   animal_id: Integer, Foreign Key -> Animal.id
#   date: Date
#   medicine_name: String
#   dosage: String
#   reason: String

Base = declarative_base()

class Animal(Base):
    __tablename__ = 'animals'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    notes = Column(String)

    milk_records = relationship('MilkRecord', back_populates='animal', cascade='all, delete-orphan')
    feed_records = relationship('FeedRecord', back_populates='animal', cascade='all, delete-orphan')
    medicine_records = relationship('MedicineRecord', back_populates='animal', cascade='all, delete-orphan')

class MilkRecord(Base):
    __tablename__ = 'milk_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    animal_id = Column(Integer, ForeignKey('animals.id'), nullable=False)
    date = Column(Date, nullable=False)
    quantity_liters = Column(Float, nullable=False)

    animal = relationship('Animal', back_populates='milk_records')

class FeedRecord(Base):
    __tablename__ = 'feed_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    animal_id = Column(Integer, ForeignKey('animals.id'), nullable=False)
    date = Column(Date, nullable=False)
    feed_type = Column(String, nullable=False)
    quantity_kg = Column(Float, nullable=False)

    animal = relationship('Animal', back_populates='feed_records')

class MedicineRecord(Base):
    __tablename__ = 'medicine_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    animal_id = Column(Integer, ForeignKey('animals.id'), nullable=False)
    date = Column(Date, nullable=False)
    medicine_name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    reason = Column(String, nullable=False)

    animal = relationship('Animal', back_populates='medicine_records')

# -----------------------------
# Database Connection & Setup
# -----------------------------
DATABASE_URL = 'sqlite:///dairy_farm.db'
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

# -----------------------------
# CRUD Operations
# -----------------------------

# Animal CRUD
# ----------

def create_animal(db_session, name, breed, date_of_birth, notes=None):
    animal = Animal(name=name, breed=breed, date_of_birth=date_of_birth, notes=notes)
    db_session.add(animal)
    db_session.commit()
    db_session.refresh(animal)
    return animal

def get_animal(db_session, animal_id):
    return db_session.query(Animal).filter(Animal.id == animal_id).first()

def get_all_animals(db_session):
    return db_session.query(Animal).all()

def update_animal(db_session, animal_id, **kwargs):
    animal = get_animal(db_session, animal_id)
    if not animal:
        return None
    for key, value in kwargs.items():
        setattr(animal, key, value)
    db_session.commit()
    return animal

def delete_animal(db_session, animal_id):
    animal = get_animal(db_session, animal_id)
    if animal:
        db_session.delete(animal)
        db_session.commit()
    return animal

# MilkRecord CRUD
# ----------------

def create_milk_record(db_session, animal_id, date, quantity_liters):
    record = MilkRecord(animal_id=animal_id, date=date, quantity_liters=quantity_liters)
    db_session.add(record)
    db_session.commit()
    db_session.refresh(record)
    return record

def get_milk_record(db_session, record_id):
    return db_session.query(MilkRecord).filter(MilkRecord.id == record_id).first()

def get_milk_by_animal(db_session, animal_id):
    return db_session.query(MilkRecord).filter(MilkRecord.animal_id == animal_id).all()

def update_milk_record(db_session, record_id, **kwargs):
    record = get_milk_record(db_session, record_id)
    if not record:
        return None
    for key, value in kwargs.items():
        setattr(record, key, value)
    db_session.commit()
    return record

def delete_milk_record(db_session, record_id):
    record = get_milk_record(db_session, record_id)
    if record:
        db_session.delete(record)
        db_session.commit()
    return record

# FeedRecord CRUD
# ----------------

def create_feed_record(db_session, animal_id, date, feed_type, quantity_kg):
    record = FeedRecord(animal_id=animal_id, date=date, feed_type=feed_type, quantity_kg=quantity_kg)
    db_session.add(record)
    db_session.commit()
    db_session.refresh(record)
    return record

def get_feed_record(db_session, record_id):
    return db_session.query(FeedRecord).filter(FeedRecord.id == record_id).first()

def get_feed_by_animal(db_session, animal_id):
    return db_session.query(FeedRecord).filter(FeedRecord.animal_id == animal_id).all()

def update_feed_record(db_session, record_id, **kwargs):
    record = get_feed_record(db_session, record_id)
    if not record:
        return None
    for key, value in kwargs.items():
        setattr(record, key, value)
    db_session.commit()
    return record

def delete_feed_record(db_session, record_id):
    record = get_feed_record(db_session, record_id)
    if record:
        db_session.delete(record)
        db_session.commit()
    return record

# MedicineRecord CRUD
# --------------------

def create_medicine_record(db_session, animal_id, date, medicine_name, dosage, reason):
    record = MedicineRecord(animal_id=animal_id, date=date,
                            medicine_name=medicine_name, dosage=dosage, reason=reason)
    db_session.add(record)
    db_session.commit()
    db_session.refresh(record)
    return record

def get_medicine_record(db_session, record_id):
    return db_session.query(MedicineRecord).filter(MedicineRecord.id == record_id).first()

def get_medicine_by_animal(db_session, animal_id):
    return db_session.query(MedicineRecord).filter(MedicineRecord.animal_id == animal_id).all()

def update_medicine_record(db_session, record_id, **kwargs):
    record = get_medicine_record(db_session, record_id)
    if not record:
        return None
    for key, value in kwargs.items():
        setattr(record, key, value)
    db_session.commit()
    return record

def delete_medicine_record(db_session, record_id):
    record = get_medicine_record(db_session, record_id)
    if record:
        db_session.delete(record)
        db_session.commit()
    return record

# Miscellenous CRUD
# --------------------

def get_all_animal_names(db: Session):
    return db.query(Animal.id, Animal.name).all()

# -----------------------------
# Utility: Session Context
# -----------------------------
@contextmanager
def get_db_session() -> Generator[Session, Any, None]:
    """
    Context manager to provide a transactional session and ensure closure.
    Usage:
        with get_db_session() as db:
            # use db
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

if __name__ == '__main__':
    # Initialize database and tables
    init_db()
    print("Database initialized and tables created.")
