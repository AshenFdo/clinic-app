from sqlalchemy import String, Integer, Numeric, Column, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base
from sqlalchemy.orm import relationship 


class MedicalHistory(Base):
    """
    Medical history model representing the medical history of patients.
    Attributes:
        patient_id (UUID): Unique identifier for the patient.
        appointment_id (UUID): Unique identifier for the appointment.
        title (String): Title of the medical history entry.
        diagnosis_notes (String): Notes about the diagnosis.
        health_status (String): Current health status of the patient.
        attachment_url (String): URL for any attachments related to the medical history entry.
    """
    __tablename__ = "MedicalHistory"


    patient_id = Column(UUID(as_uuid=True),ForeignKey("Patient.patient_id"), primary_key=True, nullable=False)
    appointment_id = Column(UUID(as_uuid=True), ForeignKey("Appointment.appointment_id"), primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    diagnosis_notes = Column(String, nullable=False)
    health_status = Column(String, nullable=False)
    attachment_url = Column(String, nullable=False)

    # Relationships
    appointment = relationship("Appointment", back_populates="medical_histories")
    patient = relationship("Patient", back_populates="medical_histories")
