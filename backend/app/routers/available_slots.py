from fastapi import APIRouter, Depends, dependencies
from app.services.available_slots_services import get_avaulable_slots, get_avaulable_slots_by_doctorID
from app.core.dependencies import get_db, get_current_user, require_role
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.available_slots import AvailableSlots
from app.schemas.available_slots import AvailableSlotsForDoctorResponse

router = APIRouter(prefix="/available-slot",tags=["Available Slots"])

# -----------------------------------
# API router to get available slots for a specific doctor
#  -----------------------------------

@router.get("/my-slots", response_model=list[AvailableSlotsForDoctorResponse], dependencies=[Depends(require_role("Doctor"))])
async def read_available_slots_for_doctor(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return await get_avaulable_slots(db, current_user)

@router.get("/doctor/{doctor_id}", response_model=list[AvailableSlotsForDoctorResponse], dependencies=[Depends(require_role("Admin"))])
async def read_available_slots_for_doctor_admin(
    doctor_id: str,
    db: AsyncSession = Depends(get_db),
):
    return await get_avaulable_slots_by_doctorID(db, doctor_id)
    