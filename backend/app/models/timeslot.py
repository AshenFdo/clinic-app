from sqlalchemy import String, Integer, Numeric, Column, Date
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base


class TimeSlot(Base):
    __tablename__ = "TimeSlot"

    """ 
    TimeSlot model representing the available time slots for appointments.
    Attributes:
        slot_id (UUID): Unique identifier for the time slot.
        day_of_week (String): Day of the week for the time slot (e.g.,
            Monday, Tuesday, etc.).
        date (Date): Date of the time slot.
        slot_time (String): Time of the time slot (e.g., 09:00 AM - 10:00 AM).
    """

    slot_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    day_of_week = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    slot_time = Column(String, nullable=False)