from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, require_role
from app.services.patient_services import get_patient_by_id
from app.models.user import User
from app.schemas.patient import PatientResponse

router = APIRouter(prefix="/patients", tags=["Patients"])

# ------------------------------------
# API router to get patient by id (admin only)
# ------------------------------------
@router.get("/{patient_id}", response_model= PatientResponse)
async def read_patient_by_id(
    patient_id: str,
    db: AsyncSession = Depends(get_db),
):
    return await get_patient_by_id(patient_id, db)