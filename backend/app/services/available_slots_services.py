from unittest import result

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from app.models.available_slots import AvailableSlots
from app.models.user import User
from app.models.timeslot import TimeSlot
from app.schemas.available_slots import  (CreateAvailableSlotRequest, 
                                          AvailableSlotsResponse,
                                          UpdateAvailableSlotRequest)

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
                expected_appointments=available_slot.expected_appointments or 0,
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
        expected_appointments=available_slot.expected_appointments or 0
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
# Function to get all available slot by id (Admin view)
# -----------------------------------
async def get_available_slot_by_id(db:AsyncSession, as_id:str):
    """
    Fetches a specific available slot by its ID from the database (Admin view)
    """
    try:
        av_slot = await db.execute(
            select(AvailableSlots,TimeSlot,User)
                .join(TimeSlot, AvailableSlots.slot_id == TimeSlot.slot_id)
                .join(User, AvailableSlots.doctor_id == User.user_id)
             .where(AvailableSlots.as_id == as_id)
            )
        result = av_slot.first()
        if not result:
            raise HTTPException(status_code=404, detail="Available slot not found")
        
        available_slot, time_slot, doctor = result
        return _map_available_slot_to_response(available_slot, time_slot, doctor)

    except HTTPException:
        raise
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
        
        # Validate Time slot time < current time (Cannot add past time slots)
        current_time = datetime.now().time()
        if time_slot.date < datetime.now().date() or (time_slot.date == datetime.now().date() and time_slot.end_time < current_time):
            raise HTTPException(status_code=400, detail="Cannot add past time slots as available.")
            
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

# -----------------------------------
# Function to update available slot for a doctor
# -----------------------------------
async def update_av_slots(db:AsyncSession,data:UpdateAvailableSlotRequest, as_id:str, doctor:User):
    """
    - Doctors can update the status of their available slots.
    - Updates the status of an existing available slot for a doctor in the database
    - 
        - Validate AvailableSlot if exists and belongs to the doctor
        - Update AvailableSlot entry
    """
    try:
        # Validate if the provided as_id exists in the AvailableSlots table and belongs to the doctor
        av_slot_result = await db.execute(
            select(AvailableSlots).where(AvailableSlots.as_id == as_id, AvailableSlots.doctor_id == doctor.user_id)
        )
        av_slot = av_slot_result.scalars().first()

        if not av_slot:
            raise HTTPException(status_code=404, detail="Available slot not found for this doctor.")
        
        # Update the status of the available slot
        update_data = data.model_dump(exclude_unset=True)
        # Update data (For now, only status can be updated, but this can be extended in the future if needed)
        for field, value in update_data.items():
            setattr(av_slot, field, value)

        await db.commit()
        await db.refresh(av_slot)

        # Fetch the related TimeSlot and Doctor information for the response
        result = await db.execute(
            select(AvailableSlots, TimeSlot, User)
            .join(TimeSlot, AvailableSlots.slot_id == TimeSlot.slot_id)
            .join(User, AvailableSlots.doctor_id == User.user_id)
            .where(AvailableSlots.as_id == as_id)
        )
        row = result.first()
        if not row:
            raise HTTPException(status_code=404, detail="Updated available slot not found.")

        available_slot, time_slot, doctor_row = row

        return _map_available_slot_to_response(available_slot, time_slot, doctor_row)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# ------------------------------------ 
# Function to delete an available slot for a doctor
# ------------------------------------
async def delete_available_slot(db:AsyncSession, as_id:str, doctor:User):
    """
    - Doctors can delete their available slots.
    - Deletes an existing available slot for a doctor from the database
    """
    try:
        # Validate Doctor if exists
        doctor_id = doctor.user_id
        if not doctor_id:
            raise HTTPException(status_code=400, detail="Doctor not found.")
        
        # Validate if the provided as_id exists in the AvailableSlots table and belongs to the doctor
        av_slot_result = await db.execute(
            select(AvailableSlots)
            .where(AvailableSlots.as_id == as_id)
            .where(AvailableSlots.doctor_id == doctor_id)
        )
        av_slot = av_slot_result.scalars().first()
        if not av_slot:
            raise HTTPException(status_code=404, detail="Available slot not found for this doctor.")
        
        # Delete the available slot
        await db.delete(av_slot)
        await db.commit()

        return "Item deleted"
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))