from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime


class Prescription(Base):
    """Prescription model representing the prescriptions table"""

    __tablename__ = "prescriptions"

    prescription_id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(String(50), nullable=False, index=True)
    patient_id = Column(Integer, nullable=False, index=True)
    doctor_id = Column(Integer, nullable=False, index=True)
    medication = Column(String(255), nullable=False)
    dosage = Column(String(50), nullable=False)
    days = Column(Integer, nullable=False)
    issued_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Prescription(prescription_id={self.prescription_id}, appointment_id={self.appointment_id})>"
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

settings = get_settings()

# Create engine with connection pooling
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

