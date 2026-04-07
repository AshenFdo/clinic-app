from pydantic import BaseModel, EmailStr,ConfigDict
from uuid import UUID
from datetime import date
from typing import Optional
from decimal import Decimal
from pydantic import field_validator

from app.schemas.user import UserResponse


class PatientResponse(BaseModel):
    """
    PatientResponse model representing the data returned in API responses about a patient.
    """
    userData: UserResponse
    patient_number: str