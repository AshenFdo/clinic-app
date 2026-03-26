from sqlalchemy import String, Integer, Numeric, Column, Date
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base


class Patient(Base):
    __tablename__ = "Patient"

    """
    Patient model representing the patients in the system.
    Attributes:
        patient_id (UUID): Unique identifier for the patient.
        patient_number (String): Unique patient number for identification.
    """

    patient_id = Column(UUID(as_uuid=True), primary_key=True)
    patient_number = Column(String, nullable=False, unique=True)