from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.timeslot import TimeSlot
from app.schemas.timeslot import TimeSlotCreateRequest, TimeSlotUpdateResponse


# -----------------------------------
# Function to create a new time slot
#  ----------------------------------- 
async def create_a_timeslot(db:AsyncSession, data: TimeSlotCreateRequest):
    try:
        if data.start_time >= data.end_time:
            raise HTTPException(status_code=400, detail="Start time must be before end time.")
        

        new_timeslot = TimeSlot(
            day_of_week=data.day_of_week,
            date=data.date,
            start_time=data.start_time,
            end_time=data.end_time
        )
        db.add(new_timeslot)
        await db.commit()
        await db.refresh(new_timeslot)

        return new_timeslot
    except Exception as e:
        print(f"Error in creating a timeslot {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException:
        raise

# -----------------------------------
# Function to delete a time slot by ID
#  -----------------------------------
async def delete_a_timeslot(db:AsyncSession, slot_id:str):
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
    try:
        result = await db.execute(select(TimeSlot).where(TimeSlot.slot_id == slot_id))
        slot = result.scalars().first()
        
        if not slot:
            raise HTTPException(status_code=404, detail="Time slot not found.")

        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="At least one field must be provided.")

        new_start_time = update_data.get("start_time", slot.start_time)
        new_end_time = update_data.get("end_time", slot.end_time)
        if new_start_time >= new_end_time:
            raise HTTPException(status_code=400, detail="Start time must be before end time.")
        
        for field, value in update_data.items():
            if value is not None:
                setattr(slot, field, value)
        await db.commit()
        await db.refresh(slot)
        return slot


    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    