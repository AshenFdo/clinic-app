from fastapi import APIRouter, Depends, dependencies
from app.core.dependencies import get_db, get_current_user, require_role
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.available_slots import AvailableSlots
from app.schemas.available_slots import (AvailableSlotsResponse,
                                         CreateAvailableSlotRequest,
                                         UpdateAvailableSlotRequest
                                         )
from app.services.available_slots_services import ( get_avaulable_slots,
                                                   get_avaulable_slots_by_doctorID,
                                                   add_available_slot,
                                                   update_av_slots,
                                                   delete_available_slot,
                                                   get_available_slot_by_id
                                                   )


router = APIRouter(prefix="/available-slot",tags=["Available Slots"])

# -----------------------------------
# API router to get available slots for a specific doctor
#  -----------------------------------

@router.get("/my-slots", response_model=list[AvailableSlotsResponse], dependencies=[Depends(require_role("Doctor"))])
async def read_available_slots_for_doctor(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return await get_avaulable_slots(db, current_user)

# Admin View
@router.get("/doctor/{doctor_id}", response_model=list[AvailableSlotsResponse]) #dependencies=[Depends(require_role("Admin"))]
async def read_available_slots_for_doctor_admin(
    doctor_id: str,
    db: AsyncSession = Depends(get_db),
):
    return await get_avaulable_slots_by_doctorID(db, doctor_id)

# 
@router.get("/{as_id}", response_model=AvailableSlotsResponse)
async def read_available_slot_by_id(
    as_id: str,
    db: AsyncSession = Depends(get_db),
):
    return await get_available_slot_by_id(db, as_id)

# -----------------------------------
# API router to add available slot for a doctor
#  -----------------------------------
@router.post("/add", response_model=AvailableSlotsResponse, dependencies=[Depends(require_role("Doctor"))])
async def create_available_slot(
    data: CreateAvailableSlotRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return await add_available_slot(db, current_user, data)

# ------------------------------------
# API router to update available slot for a doctor
# ------------------------------------
@router.patch("/update/{as_id}", response_model=AvailableSlotsResponse, dependencies=[Depends(require_role("Doctor"))])
async def update_available_slot(
    as_id: str,
    data: UpdateAvailableSlotRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return await update_av_slots(db, data, as_id, current_user)

# ------------------------------------
# API router to delete available slot for a doctor
# ------------------------------------
@router.delete("/delete/{as_id}", dependencies=[Depends(require_role("Doctor"))])
async def delete_av_slot(
    as_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return await delete_available_slot(db, as_id, current_user)

