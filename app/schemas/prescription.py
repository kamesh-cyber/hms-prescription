from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


class PrescriptionBase(BaseModel):
    """Base prescription schema"""
    appointment_id: int = Field(..., gt=0, description="Appointment ID")
    patient_id: int = Field(..., gt=0, description="Patient ID")
    doctor_id: int = Field(..., gt=0, description="Doctor ID")
    medication: str = Field(..., min_length=1, max_length=255, description="Medication name")
    dosage: str = Field(..., min_length=1, max_length=50, description="Dosage (e.g., 0-1-1)")
    days: int = Field(..., gt=0, le=365, description="Number of days")

    @validator('dosage')
    def validate_dosage(cls, v):
        """Validate dosage format (e.g., 0-1-1)"""
        if not v:
            raise ValueError('Dosage cannot be empty')
        # Optional: Add specific dosage format validation
        return v


class PrescriptionCreate(PrescriptionBase):
    """Schema for creating a prescription"""
    issued_at: Optional[datetime] = None


class PrescriptionResponse(PrescriptionBase):
    """Schema for prescription response"""
    prescription_id: int
    issued_at: datetime

    class Config:
        from_attributes = True


class PrescriptionListResponse(BaseModel):
    """Schema for listing prescriptions"""
    total: int
    prescriptions: list[PrescriptionResponse]

