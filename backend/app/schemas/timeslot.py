from uuid import UUID

from datetime import date as DateType, time as TimeType
from typing import Optional

from pydantic import BaseModel, ConfigDict

class TimeSlotCreateRequest(BaseModel):
    """
    TimeSlotCreateRequest model representing the data required to create a new time slot.
    This is the payload expected when creating a new time slot for a doctor.
    """
    day_of_week: str
    date: DateType
    room_no: str
    start_time: TimeType
    end_time: TimeType

class TimeSlotResponse(BaseModel):
    slot_id: UUID
    day_of_week: str
    date: DateType
    room_no: str
    start_time: TimeType
    end_time: TimeType

    model_config = ConfigDict(from_attributes=True)

class TimeSlotUpdateResponse(BaseModel):
    day_of_week: Optional[str] = None
    date: Optional[DateType] = None
    room_no: Optional[str] = None
    start_time: Optional[TimeType] = None
    end_time: Optional[TimeType] = None