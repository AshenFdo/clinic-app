from sqlalchemy import String, Integer, Numeric, Column, Date,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base
from sqlalchemy.orm import relationship


class Patient(Base):
    """
    Patient model representing the patients in the system.
    Attributes:
        patient_id (UUID): Unique identifier for the patient.
        patient_number (String): Unique patient number for identification.
    """
    __tablename__ = "Patient"
    
    patient_id = Column(UUID(as_uuid=True), ForeignKey("User.user_id"), primary_key=True)
    patient_number = Column(String, nullable=False, unique=True)

    # Relationships
    user = relationship("User", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")
    medical_histories = relationship("MedicalHistory", back_populates="patient")
    prescriptions = relationship("Prescription", back_populates="patient")
