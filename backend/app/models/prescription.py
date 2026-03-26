from sqlalchemy import String, Integer, Numeric, Column, Date,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base
from sqlalchemy.orm import relationship

class Prescription(Base):
    """
    Prescription model representing the prescriptions for patients.
    Attributes:
        prescription_id (UUID): Unique identifier for the prescription.
        doctor_id (UUID): Identifier for the doctor who created the prescription.
        patient_id (UUID): Identifier for the patient for whom the prescription is created.
        appointment_id (UUID): Identifier for the appointment related to the prescription.
        title (String): Title of the prescription.
        status (String): Status of the prescription (e.g., active, inactive, deleted).

    """
    __tablename__ = "Prescription"

    prescription_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("Doctor.doctor_id"), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("Patient.patient_id"), nullable=False)
    appointment_id = Column(UUID(as_uuid=True), ForeignKey("Appointment.appointment_id"), nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, nullable=False)


    # Relationships
    doctor = relationship("Doctor", back_populates="prescriptions")
    patient = relationship("Patient", back_populates="prescriptions")
    appointment = relationship("Appointment", back_populates="prescriptions")
    prescription_items = relationship("PrescriptionItem", back_populates="prescription")
