from sqlalchemy import Boolean, String,  Column, Date,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base
from sqlalchemy.orm import relationship


class Appointment(Base):
    """
    Appointment model representing the doctor appointments in the system.
    Attributes:
        appointment_id (UUID): Unique identifier for the appointment.
        doctor_id (UUID): Unique identifier for the doctor.
        patient_id (UUID): Unique identifier for the patient.
        as_id (UUID): Unique identifier for the available slot.
        status (String): Status of the appointment (e.g., Scheduled, Completed, Cancelled).
        mode (String): Mode of the appointment (e.g., In-person, Telemedicine).
        is_draft (Boolean): Indicates if the appointment is a draft (True) or finalized (False).
    """

    __tablename__ = "Appointment"
    
    appointment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("Doctor.doctor_id"), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("Patient.patient_id"), nullable=False)
    as_id = Column(UUID(as_uuid=True), ForeignKey("AvailableSlots.as_id"), nullable=False)
    status = Column(String, nullable=False)
    mode = Column(String, nullable=False)
    is_draft = Column(Boolean, default=True)


    # Relationships
    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    medical_histories = relationship("MedicalHistory", back_populates="appointment", uselist=False)
    prescriptions = relationship("Prescription", back_populates="appointment")
    available_slots = relationship("AvailableSlots", back_populates="appointments")
