from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.room import Room


# -----------------------------------
# Function to get all rooms 
#  -----------------------------------
async def get_all_rooms(db: AsyncSession):
    try:
        result = await db.execute(select(Room))
        rooms = result.scalars().all()
        return rooms
    
    except Exception as e:
        print(f"Error in getting all rooms {e}")
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------------
# Function to get a room by ID
#  -----------------------------------


# -----------------------------------
# Function to create a new room
#  -----------------------------------


# -----------------------------------
# Function to update a room by ID
#  -----------------------------------

# -----------------------------------
# Function to delete a room by ID
#  -----------------------------------
