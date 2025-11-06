from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.prescription import (
    PrescriptionCreate,
    PrescriptionResponse,
    PrescriptionListResponse
)
from app.services.prescription_service import PrescriptionService

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"])


@router.post(
    "/",
    response_model=PrescriptionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new prescription"
)
def create_prescription(
    prescription: PrescriptionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new prescription for an appointment.

    - **appointment_id**: ID of the appointment (required)
    - **patient_id**: ID of the patient
    - **doctor_id**: ID of the doctor
    - **medication**: Name of the medication
    - **dosage**: Dosage format (e.g., 0-1-1)
    - **days**: Number of days for the prescription
    - **issued_at**: Timestamp when prescription was issued (optional, defaults to current time)

    Note: Prescription cannot be created without a valid appointment.
    """
    try:
        db_prescription = PrescriptionService.create_prescription(db, prescription)
        return db_prescription
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create prescription: {str(e)}"
        )


@router.get(
    "/{prescription_id}",
    response_model=PrescriptionResponse,
    summary="Get a prescription by ID"
)
def get_prescription(
    prescription_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific prescription by its ID.

    - **prescription_id**: The ID of the prescription to retrieve
    """
    db_prescription = PrescriptionService.get_prescription(db, prescription_id)

    if db_prescription is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prescription with ID {prescription_id} not found"
        )

    return db_prescription


@router.get(
    "/",
    response_model=PrescriptionListResponse,
    summary="Get prescriptions with optional filters"
)
def get_prescriptions(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return"),
    patient_id: Optional[int] = Query(None, description="Filter by patient ID"),
    doctor_id: Optional[int] = Query(None, description="Filter by doctor ID"),
    appointment_id: Optional[int] = Query(None, description="Filter by appointment ID"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of prescriptions with optional filters.

    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **patient_id**: Filter prescriptions by patient ID
    - **doctor_id**: Filter prescriptions by doctor ID
    - **appointment_id**: Filter prescriptions by appointment ID
    """
    prescriptions, total = PrescriptionService.get_prescriptions(
        db=db,
        skip=skip,
        limit=limit,
        patient_id=patient_id,
        doctor_id=doctor_id,
        appointment_id=appointment_id
    )

    return PrescriptionListResponse(
        total=total,
        prescriptions=prescriptions
    )


@router.get(
    "/patient/{patient_id}",
    response_model=PrescriptionListResponse,
    summary="Get all prescriptions for a patient"
)
def get_patient_prescriptions(
    patient_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Retrieve all prescriptions for a specific patient.

    - **patient_id**: The ID of the patient
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    prescriptions, total = PrescriptionService.get_prescriptions_by_patient(
        db=db,
        patient_id=patient_id,
        skip=skip,
        limit=limit
    )

    return PrescriptionListResponse(
        total=total,
        prescriptions=prescriptions
    )


@router.get(
    "/doctor/{doctor_id}",
    response_model=PrescriptionListResponse,
    summary="Get all prescriptions issued by a doctor"
)
def get_doctor_prescriptions(
    doctor_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Retrieve all prescriptions issued by a specific doctor.

    - **doctor_id**: The ID of the doctor
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    prescriptions, total = PrescriptionService.get_prescriptions_by_doctor(
        db=db,
        doctor_id=doctor_id,
        skip=skip,
        limit=limit
    )

    return PrescriptionListResponse(
        total=total,
        prescriptions=prescriptions
    )


@router.get(
    "/appointment/{appointment_id}/prescriptions",
    response_model=list[PrescriptionResponse],
    summary="Get all prescriptions for an appointment"
)
def get_appointment_prescriptions(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve all prescriptions for a specific appointment.

    - **appointment_id**: The ID of the appointment
    """
    prescriptions = PrescriptionService.get_prescriptions_by_appointment(
        db=db,
        appointment_id=appointment_id
    )

    return prescriptions

