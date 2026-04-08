from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.dependencies import get_db , require_role
from app.services.timeslot_services import create_a_timeslot, delete_a_timeslot, get_all_timeslots, update_time_slot
from app.schemas.timeslot import TimeSlotCreateRequest,TimeSlotResponse, TimeSlotUpdateResponse

router = APIRouter(prefix="/timeslot", tags=["TimeSlot"])

# -----------------------------------
# API router to create a new time slot
# -----------------------------------
@router.post("/create", response_model=TimeSlotCreateRequest)
async def create_timeslot(
    data: TimeSlotCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    return await create_a_timeslot(db, data)

# -----------------------------------
# API router to delete a time slot by ID
# -----------------------------------
@router.delete("/delete/{slot_id}")
async def delete_timeslot(
    slot_id: str,
    db: AsyncSession = Depends(get_db),
):
    return await delete_a_timeslot(db, slot_id)

# -----------------------------------
# API router to get all time slots
# -----------------------------------
@router.get("/all", response_model=list[TimeSlotResponse])
async def read_all_timeslots(
    db: AsyncSession = Depends(get_db),
):
    return await get_all_timeslots(db)



# -----------------------------------
# API router to update a time slot by ID
# -----------------------------------
@router.patch("/update/{slot_id}", response_model=TimeSlotResponse)
async def update_timeslot(
    slot_id: UUID,
    data: TimeSlotUpdateResponse,
    db: AsyncSession = Depends(get_db),
    
):
    return await update_time_slot(db, data, slot_id)