from sqlalchemy import String, Integer, Numeric, Column, Date,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from sqlalchemy.orm import relationship




class Doctor(Base):
    """
    Doctor model representing the doctor table  in the system.
    Attributes:
        doctor_id (UUID): Unique identifier for the doctor.
        professional_bio (String): Professional biography of the doctor.
        specialty (String): Medical specialty of the doctor.
        years_of_experience (Integer): Number of years of experience the doctor has.
    """
    __tablename__ = "Doctor"

    doctor_id = Column(UUID(as_uuid=True), ForeignKey("User.user_id"), primary_key=True)
    professional_bio = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    years_of_experience = Column(Integer, nullable=False)

    # Relationships
    user = relationship("User", back_populates="doctor")
    available_slots = relationship("AvailableSlots", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
    prescriptions = relationship("Prescription", back_populates="doctor")
