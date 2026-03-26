from sqlalchemy import String, Integer, Numeric, Column, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from app.models.base import Base


class AvailableSlots(Base):

    """
    Available slots model representing the available time slots for appointments.
    Attributes:
        as_id (UUID): Unique identifier for the available slot.
        doctor_id (UUID): Unique identifier for the doctor.
        room_id (UUID): Unique identifier for the room.
        slot_id (UUID): Unique identifier for the time slot.
        status (String): Status of the available slot (e.g., Available, Booked, Unavailable).
    """
    __tablename__ = "AvailableSlots"

    as_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("Doctor.doctor_id"), nullable=False)
    room_id = Column(UUID(as_uuid=True), ForeignKey("Room.room_id"), nullable=False)
    slot_id = Column(UUID(as_uuid=True), ForeignKey("TimeSlot.slot_id"), nullable=False)
    status = Column(String, nullable=False)


    # Relationships
    doctor = relationship("Doctor", back_populates="available_slots")
    room = relationship("Room", back_populates="available_slots")
    time_slot = relationship("TimeSlot", back_populates="available_slots")
    appointments = relationship("Appointment", back_populates="available_slots")


