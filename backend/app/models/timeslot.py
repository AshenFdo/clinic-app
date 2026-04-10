from sqlalchemy import String, Column, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base


class TimeSlot(Base):
    """ 
    TimeSlot model representing the available time slots for appointments.
    Attributes:
        slot_id (UUID): Unique identifier for the time slot.
        day_of_week (String): Day of the week for the time slot (e.g.,
            Monday, Tuesday, etc.).
        date (Date): Date of the time slot.
        start_time (Time): Start time of the time slot (e.g., 09:00 AM).
        end_time (Time): End time of the time slot (e.g., 10:00 AM).
    """
    __tablename__ = "TimeSlot"

    slot_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    day_of_week = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    room_no = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    # Relationships
    available_slots = relationship("AvailableSlots", back_populates="time_slot")