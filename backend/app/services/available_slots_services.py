from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.available_slots import AvailableSlots
from app.models.user import User
from app.models.timeslot import TimeSlot
from app.schemas.available_slots import  CreateAvailableSlotRequest, AvailableSlotsResponse

# -----------------------------------
# Helper function to map database results to response model
# -----------------------------------

# Helper function to get available slots for a specific doctor
def _map_available_slots_to_response(results) -> list[AvailableSlotsResponse]:
    data: list[AvailableSlotsResponse] = []
    for available_slot, time_slot, doctor in results:
        data.append(
            AvailableSlotsResponse(
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


def _map_available_slot_to_response(
    available_slot: AvailableSlots,
    time_slot: TimeSlot,
    doctor: User,
) -> AvailableSlotsResponse:
    return AvailableSlotsResponse(
        as_id=available_slot.as_id,
        doctor_name=doctor.full_name,
        room_no=time_slot.room_no,
        day_of_week=time_slot.day_of_week,
        date=time_slot.date,
        start_time=time_slot.start_time,
        end_time=time_slot.end_time,
        status=available_slot.status or "Available",
    )


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
    """
    Fetches available slots for a specific doctor by doctor ID from the database (Admin view)
    """
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
async def add_available_slot(db:AsyncSession, doctor:User, data:CreateAvailableSlotRequest):
    """
    - Doctors can set their available slots by providing the necessary details.
    - Adds a new available slot for a doctor to the database
    - 
        - Validate Doctor if exists
        - Validate TimeSlot if exists
        - Create AvailableSlot entry
    """

    try:
        doctor_id = doctor.user_id
        if not doctor_id:
            raise HTTPException(status_code=400, detail="Doctor not found.")

        # Validate if the provided slot_id exists in the TimeSlot table
        slot_result = await db.execute(
            select(TimeSlot).where(TimeSlot.slot_id == data.slot_id)
            )
        time_slot = slot_result.scalars().first()

        if not time_slot:
            raise HTTPException(status_code=400, detail="The provided time slot does not exist.")

        # Validate if the slot is already marked as available for this doctor or Other doctor 
        existing_result = await db.execute(
            select(AvailableSlots).where(AvailableSlots.slot_id == data.slot_id)
        )
        existing_slots = existing_result.scalars().all()

        for slot in existing_slots:
            if slot.doctor_id != doctor_id:
                raise HTTPException(status_code=400, detail="This time slot is already marked as available for another doctor.")
            raise HTTPException(status_code=400, detail="This time slot is already marked as available for this doctor.")
            
        # Create a new AvailableSlots entry
        new_av_slot = AvailableSlots(
            doctor_id = doctor_id,
            slot_id = data.slot_id,
            status = data.status
        )

        db.add(new_av_slot)
        await db.commit()
        await db.refresh(new_av_slot)

        return _map_available_slot_to_response(new_av_slot, time_slot, doctor)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



    