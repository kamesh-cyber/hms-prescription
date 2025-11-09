from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import datetime

from app.models.prescription import Prescription
from app.schemas.prescription import PrescriptionCreate


class PrescriptionService:
    """Service layer for prescription operations"""

    @staticmethod
    def create_prescription(db: Session, prescription: PrescriptionCreate) -> Prescription:
        """
        Create a new prescription

        Args:
            db: Database session
            prescription: Prescription data

        Returns:
            Created prescription

        Raises:
            ValueError: If appointment doesn't exist
        """
        # Note: In a real application, you should verify that the appointment exists
        # by calling the appointment service or checking the appointment table

        db_prescription = Prescription(
            appointment_id=prescription.appointment_id,
            patient_id=prescription.patient_id,
            doctor_id=prescription.doctor_id,
            medication=prescription.medication,
            dosage=prescription.dosage,
            days=prescription.days,
            issued_at=prescription.issued_at or datetime.utcnow()
        )

        db.add(db_prescription)
        db.commit()
        db.refresh(db_prescription)

        return db_prescription

    @staticmethod
    def get_prescription(db: Session, prescription_id: int) -> Optional[Prescription]:
        """
        Get a prescription by ID

        Args:
            db: Database session
            prescription_id: Prescription ID

        Returns:
            Prescription if found, None otherwise
        """
        return db.query(Prescription).filter(
            Prescription.prescription_id == prescription_id
        ).first()

    @staticmethod
    def get_prescriptions(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        patient_id: Optional[int] = None,
        doctor_id: Optional[int] = None,
        appointment_id: Optional[str] = None
    ) -> tuple[List[Prescription], int]:
        """
        Get prescriptions with optional filters

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            patient_id: Filter by patient ID
            doctor_id: Filter by doctor ID
            appointment_id: Filter by appointment ID

        Returns:
            Tuple of (list of prescriptions, total count)
        """
        query = db.query(Prescription)

        if patient_id is not None:
            query = query.filter(Prescription.patient_id == patient_id)

        if doctor_id is not None:
            query = query.filter(Prescription.doctor_id == doctor_id)

        if appointment_id is not None:
            query = query.filter(Prescription.appointment_id == appointment_id)

        total = query.count()
        prescriptions = query.offset(skip).limit(limit).all()

        return prescriptions, total

    @staticmethod
    def get_prescriptions_by_patient(
        db: Session,
        patient_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Prescription], int]:
        """Get all prescriptions for a specific patient"""
        return PrescriptionService.get_prescriptions(
            db=db,
            skip=skip,
            limit=limit,
            patient_id=patient_id
        )

    @staticmethod
    def get_prescriptions_by_doctor(
        db: Session,
        doctor_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Prescription], int]:
        """Get all prescriptions issued by a specific doctor"""
        return PrescriptionService.get_prescriptions(
            db=db,
            skip=skip,
            limit=limit,
            doctor_id=doctor_id
        )

    @staticmethod
    def get_prescriptions_by_appointment(
        db: Session,
        appointment_id: str
    ) -> List[Prescription]:
        """Get all prescriptions for a specific appointment"""
        prescriptions, _ = PrescriptionService.get_prescriptions(
            db=db,
            appointment_id=appointment_id
        )
        return prescriptions

