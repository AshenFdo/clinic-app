from pydantic import BaseModel
from typing import Optional
from datetime import date , time

class TimeSlotCreateRequest(BaseModel):
    """
    TimeSlotCreateRequest model representing the data required to create a new time slot.
    This is the payload expected when creating a new time slot for a doctor.
    """
    day_of_week: str
    date: date
    start_time: time
    end_time: time