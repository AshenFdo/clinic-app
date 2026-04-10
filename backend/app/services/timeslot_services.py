from uuid import UUID

from fastapi import HTTPException
from httpx import get
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.timeslot import TimeSlot
from app.schemas.timeslot import TimeSlotCreateRequest, TimeSlotUpdateResponse

# --------------------------------
# Helper functions
# --------------------------------

# Helper function to check if two time slots overlap
def _slots_overlap(existing_slot: TimeSlot, date, start_time, end_time) -> bool:
    return (
        existing_slot.date == date
        and start_time < existing_slot.end_time
        and end_time > existing_slot.start_time
    )


# -----------------------------------
# Function to create a new time slot
#  ----------------------------------- 
async def create_a_timeslot(db:AsyncSession, data: TimeSlotCreateRequest):
    """
    Creates a new time slot in the database after validating the input data and checking for overlapping time slots.
    """
    try:
        # Validate that the start time is before the end time
        if data.start_time >= data.end_time:
            raise HTTPException(status_code=400, detail="Start time must be before end time.")

        # Get all existing time slots to check for overlaps
        timeslots = await get_all_timeslots(db)

        # Check for overlapping time slots
        for slot in timeslots:
            if _slots_overlap(slot, data.date, data.start_time, data.end_time):
                raise HTTPException(status_code=400, detail=f"Time slot overlaps with an existing slot. {slot.start_time} - {slot.end_time} on {slot.date}")

        # Create a new time slot instance with the provided data
        new_timeslot = TimeSlot(
            day_of_week=data.day_of_week,
            date=data.date,
            room_no=data.room_no,
            start_time=data.start_time,
            end_time=data.end_time
        )

        # Add the new time slot to the database
        db.add(new_timeslot)
        # Commit the changes to the database and refresh the new time slot instance to get the generated slot_id
        await db.commit()
        await db.refresh(new_timeslot)

        return new_timeslot
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in creating a timeslot {e}")
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------------
# Function to delete a time slot by ID
#  -----------------------------------
async def delete_a_timeslot(db:AsyncSession, slot_id:str):
    """
    Deletes a time slot from the database based on the provided slot_id after validating its existence.
    """
    try:
        # Fetch once and keep values before deleting the row.
        result = await db.execute(select(TimeSlot).where(TimeSlot.slot_id == slot_id))
        slot = result.scalars().first()

        if not slot:
            raise HTTPException(status_code=404, detail="Time slot not found.")

        start_time = slot.start_time
        end_time = slot.end_time

        # Delete the time slot using the slot_id
        stmt = delete(TimeSlot).where(TimeSlot.slot_id == slot_id)
        await db.execute(stmt)
        await db.commit()

        return {"message": f"Time slot {start_time} - {end_time} has been deleted."}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in deleting a timeslot {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
# -----------------------------------
# Function to get all time slots
# -----------------------------------
async def get_all_timeslots(db: AsyncSession):
    """Fetches all time slots from the database and returns them as a list."""
    try:
        result = await db.execute(select(TimeSlot))
        result = result.scalars().all()

        if not result:
            return []
        return result

    except Exception as e:
        print(f"Error in getting all timeslots {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

# -----------------------------------
# Function to update a time slot by ID
#  -----------------------------------
async def update_time_slot(db: AsyncSession, data: TimeSlotUpdateResponse, slot_id: UUID):
    """
    Updates a time slot in the database based on the provided slot_id and update data.
     - Fetches the existing time slot from the database using the slot_id.
     - Validates the input data, checks for overlapping time slots, and updates the time slot if all checks pass.
     - Returns the updated time slot.

    """
    try:
        # Fetch the existing time slot from the database using the slot_id
        result = await db.execute(select(TimeSlot).where(TimeSlot.slot_id == slot_id))
        slot = result.scalars().first()
        
        # if the time slot does not exist, raise a 404 error
        if not slot:
            raise HTTPException(status_code=404, detail="Time slot not found.")

        # Update data
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="At least one field must be provided.")

        # Checking start_time and end_time if they are being updated, and validating them
        new_start_time = update_data.get("start_time", slot.start_time)
        new_end_time = update_data.get("end_time", slot.end_time)
        if new_start_time >= new_end_time:
            raise HTTPException(status_code=400, detail="Start time must be before end time.")

        # Checking for overlapping time slots if date, start_time, or end_time are being updated
        new_date = update_data.get("date", slot.date)
        timeslots = await get_all_timeslots(db)
        for existing_slot in timeslots:
            if existing_slot.slot_id != slot.slot_id and _slots_overlap(existing_slot, new_date, new_start_time, new_end_time):
                raise HTTPException(status_code=400, detail=f"Time slot overlaps with an existing slot. {existing_slot.start_time} - {existing_slot.end_time} on {existing_slot.date}")
        
        # Update the time slot with the new values
        for field, value in update_data.items():
            if value is not None:
                setattr(slot, field, value)
        
        # Commit the changes to the database and refresh the slot instance to get the updated values
        await db.commit()
        await db.refresh(slot)
        # Return the updated time slot
        return slot


    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    