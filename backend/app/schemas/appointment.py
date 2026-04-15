from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class CreateAppointmentRequest(BaseModel):
    """Request model for creating an appointment."""
    doctor_id: Optional[UUID] = None
    patient_id: Optional[UUID] = None
    as_id: UUID
    status: str
    mode: str

    model_config = ConfigDict(from_attributes=True)


class AppointmentResponse(BaseModel):
    """Response model for an appointment."""
    appointment_id: UUID
    doctor_id: UUID
    patient_id: Optional[UUID] = None
    as_id: UUID
    status: str
    mode: str
    is_draft: bool

    model_config = ConfigDict(from_attributes=True)

class AppointmentDetailsResponse(AppointmentResponse):
    """Detailed response model for an appointment, including related doctor and patient info."""
    doctor_name: str
    patient_name: str
    slot_time: str
    slot_date: date
