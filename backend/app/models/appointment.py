from sqlalchemy import Boolean, String, Integer, Numeric, Column, Date
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base

class Appointment(Base):
    __tablename__ = "Appointment"


    """
    Appointment model representing the appointments in the system.
    Attributes:
        appointment_id (UUID): Unique identifier for the appointment.
        doctor_id (UUID): Unique identifier for the doctor.
        patient_id (UUID): Unique identifier for the patient.
        as_id (UUID): Unique identifier for the available slot.
        status (String): Status of the appointment (e.g., Scheduled, Completed, Cancelled).
        mode (String): Mode of the appointment (e.g., In-person, Telemedicine).
        is_draft (Boolean): Indicates if the appointment is a draft (True) or finalized (False).
    """
    appointment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True), nullable=False)
    patient_id = Column(UUID(as_uuid=True), nullable=False)
    as_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(String, nullable=False)
    mode = Column(String, nullable=False)
    is_draft = Column(Boolean, default=True)