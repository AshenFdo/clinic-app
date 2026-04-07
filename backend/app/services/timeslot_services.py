from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.timeslot import TimeSlot
from app.schemas.timeslot import TimeSlotCreateRequest


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




# -----------------------------------
# Function to get all time slots
# -----------------------------------


    