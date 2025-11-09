import csv
import os
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import engine, Base
from app.models.prescription import Prescription
from app.config import get_settings

settings = get_settings()


def wait_for_db(max_retries: int = 30, delay: int = 2):
    """Wait for database to be ready"""
    import time
    from sqlalchemy import create_engine
    from sqlalchemy.exc import OperationalError

    retries = 0
    while retries < max_retries:
        try:
            print(f"Connecting to database at {settings.database_url}...")
            test_engine = create_engine(settings.database_url)
            with test_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✓ Database is ready")
            test_engine.dispose()
            return True
        except OperationalError:
            retries += 1
            print(f"Waiting for database... ({retries}/{max_retries})")
            time.sleep(delay)

    raise Exception("Database is not available")


def init_db():
    """Initialize database schema"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")


def seed_prescriptions(db: Session, csv_file_path: str):
    """
    Seed prescription data from CSV file

    Args:
        db: Database session
        csv_file_path: Path to CSV file containing prescription data
    """
    if not os.path.exists(csv_file_path):
        print(f"⚠ CSV file not found: {csv_file_path}")
        return

    print(f"Seeding prescriptions from {csv_file_path}...")

    # Check if data already exists
    existing_count = db.query(Prescription).count()
    if existing_count > 0:
        print(f"⚠ Database already contains {existing_count} prescriptions. Skipping seed.")
        return

    prescriptions = []

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            # Parse datetime
            issued_at = datetime.strptime(row['issued_at'], '%Y-%m-%d %H:%M:%S')

            prescription = Prescription(
                prescription_id=int(row['prescription_id']),
                appointment_id=str(row['appointment_id']),
                patient_id=int(row['patient_id']),
                doctor_id=int(row['doctor_id']),
                medication=row['medication'],
                dosage=row['dosage'],
                days=int(row['days']),
                issued_at=issued_at
            )
            prescriptions.append(prescription)

    # Bulk insert
    db.bulk_save_objects(prescriptions)
    db.commit()

    print(f"✓ Seeded {len(prescriptions)} prescriptions")


def setup_database():
    """Complete database setup: wait, initialize, and seed"""
    from app.database import SessionLocal

    # Wait for database to be ready
    wait_for_db()

    # Create tables
    init_db()

    # Seed data
    db = SessionLocal()
    try:
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'seed_data', 'hms_prescriptions.csv')
        seed_prescriptions(db, csv_path)
    finally:
        db.close()

    print("✓ Database setup complete")


if __name__ == "__main__":
    setup_database()

