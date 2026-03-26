from sqlalchemy import String, Integer, Numeric, Column, Date
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base
from sqlalchemy.orm import relationship

class Room(Base):
    """
    Room model representing the rooms in the clinic.
    Attributes:
        room_id (UUID): Unique identifier for the room.
        room_num (String): Room number, unique for each room.
        status (String): Status of the room (e.g., available, occupied, under maintenance).
    """
    __tablename__ = "Room"

    room_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_num = Column(String, nullable=False, unique=True)
    status = Column(String, nullable=True)

    # Relationships
    available_slots = relationship("AvailableSlots", back_populates="room")