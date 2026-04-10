from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.available_slots import AvailableSlots
from app.models.user import User
from app.models.timeslot import TimeSlot
from app.schemas.available_slots import AvailableSlotsForDoctorResponse


# Helper function to get available slots for a specific doctor
def _map_available_slots_to_response(results) -> list[AvailableSlotsForDoctorResponse]:
    data: list[AvailableSlotsForDoctorResponse] = []
    for available_slot, time_slot, doctor in results:
        data.append(
            AvailableSlotsForDoctorResponse(
                as_id=available_slot.as_id,
                doctor_name=doctor.full_name,
                room_no=time_slot.room_no,
                day_of_week=time_slot.day_of_week,
                date=time_slot.date,
                start_time=time_slot.start_time,
                end_time=time_slot.end_time,
                status=available_slot.status or "Available"
            )
        )
    return data

# -----------------------------------
# Function to get available slots for a specific doctor
# -----------------------------------
async def get_avaulable_slots(db:AsyncSession, current_doctor:User):
    """
    Fetches available slots for the currently authenticated doctor from the database
    """
    try:
        doctor  = current_doctor.user_id
        results = await db.execute(
            select(AvailableSlots, TimeSlot,User)
            .join(TimeSlot, AvailableSlots.slot_id == TimeSlot.slot_id)
            .join(User, AvailableSlots.doctor_id == User.user_id)
            .where(AvailableSlots.doctor_id == doctor)
        )   
        results = results.all()
        return _map_available_slots_to_response(results)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------------
# Function to get available slots for a specific doctor (Admin view)
# -----------------------------------
async def get_avaulable_slots_by_doctorID(db:AsyncSession, doctor_id:str):
    try:
        av_slots = await db.execute(
            select(AvailableSlots,TimeSlot,User)
                .join(TimeSlot, AvailableSlots.slot_id == TimeSlot.slot_id)
                .join(User, AvailableSlots.doctor_id == User.user_id)
             .where(AvailableSlots.doctor_id == doctor_id)
            )
        return _map_available_slots_to_response(av_slots.all())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------
# Function to add available slot for a doctor
# -----------------------------------
async def add_available_slot(db:AsyncSession, doctor:User, data):
    pass