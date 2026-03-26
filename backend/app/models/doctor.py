from sqlalchemy import String, Integer, Numeric, Column, Date
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base



class Doctor(Base):
    __tablename__ = "Doctor"

    """
    Doctor model representing the doctors in the system.
    Attributes:
        doctor_id (UUID): Unique identifier for the doctor.
        professional_bio (String): Professional biography of the doctor.
        specialty (String): Medical specialty of the doctor.
        years_of_experience (Integer): Number of years of experience the doctor has.
    """

    doctor_id = Column(UUID(as_uuid=True), primary_key=True)
    professional_bio = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    years_of_experience = Column(Integer, nullable=False)