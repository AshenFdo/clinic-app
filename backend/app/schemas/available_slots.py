from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import date as Date, time as Time



class AvailableSlotsResponse(BaseModel):
    """Response model for available slots. (Admin viwe)"""
    as_id: UUID
    doctor_name: str
    room_no:str
    date: Date
    day_of_week:str
    start_time:Time
    end_time:Time  
    status: str

    model_config = ConfigDict(from_attributes=True)


# class AvailableSlotsForDoctorResponse(BaseModel):
#     """Response model for available slots for a specific doctor."""
#     as_id: UUID
#     doctor_name: str
#     room_no:str
#     date: Date
#     day_of_week:str
#     start_time:Time
#     end_time:Time  
#     status: str

#     model_config = ConfigDict(from_attributes=True)


class CreateAvailableSlotRequest(BaseModel):
    """Request model for creating an available slot."""
    slot_id: UUID  
    status: str

    model_config = ConfigDict(from_attributes=True)

class UpdateAvailableSlotRequest(BaseModel):
    """Request model for updating an available slot
    - only status can be updated
    """
    status:str