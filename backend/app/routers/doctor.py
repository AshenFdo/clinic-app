from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db , require_role
from app.services.doctor_services import get_doctors, get_doctor_by_id,update_doctor_data,delete_doctor
from app.models.user import User
from app.schemas.doctor import DoctorResponse, DoctorUpdateRequest, MockResponse

router = APIRouter(prefix="/doctors", tags=["Doctors"])

# ------------------------------------
# API router to get all doctors
# ------------------------------------


@router.get("/", response_model=list[DoctorResponse])
async def read_doctors(
    db: AsyncSession = Depends(get_db)
):
    return await get_doctors(db)


@router.get("/{doctor_id}", response_model=DoctorResponse)
async def read_doctor_by_id(
    doctor_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await get_doctor_by_id(db, doctor_id)


@router.patch("/me", response_model=DoctorUpdateRequest)
async def update_doctor_profile(
    data: DoctorUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("Doctor")),
) :
    return await update_doctor_data(db, data, current_user)


@router.delete("/me", response_model=MockResponse)
async def delete_doctor_profile(
    db:AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("Doctor"))
):
    return await delete_doctor(db,current_user)

@router.delete("/{doctor_id}", response_model=MockResponse)
async def delete_doctor_by_id(
    doctor_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    # Implementation for deleting a doctor by ID
    pass