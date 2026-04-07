from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db , require_role
from app.services.timeslot_services import create_a_timeslot
from app.schemas.timeslot import TimeSlotCreateRequest

router = APIRouter(prefix="/timeslot", tags=["TimeSlots"])

# -----------------------------------
# API router to create a new time slot
# -----------------------------------
@router.post("/create", response_model=TimeSlotCreateRequest)
async def create_timeslot(
    data: TimeSlotCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    return await create_a_timeslot(db, data)