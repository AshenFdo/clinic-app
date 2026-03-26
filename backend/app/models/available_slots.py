from sqlalchemy import String, Integer, Numeric, Column, Date
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base


class Available_Slots(Base):
    __tablename__ = "Available_Slots"

    """
    Available slots model representing the available time slots for appointments.
    Attributes:
        as_id (UUID): Unique identifier for the available slot.
        doctor_id (UUID): Unique identifier for the doctor.
        room_id (UUID): Unique identifier for the room.
        slot_id (UUID): Unique identifier for the time slot.
        status (String): Status of the available slot (e.g., Available, Booked, Unavailable).
    """
    as_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True), nullable=False)
    room_id = Column(UUID(as_uuid=True), nullable=False)
    slot_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(String, nullable=False)
