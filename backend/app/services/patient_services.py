from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserUpdateRequest
from app.schemas.patient import PatientResponse
from app.models.doctor import Doctor
from app.models.patient import Patient

# -----------------------------------
# Function to get patient by id (admin only)
#  -----------------------------------
async def get_patient_by_id(patient_id: str, db: AsyncSession):
    try:
        result = await db.execute(
            select(Patient,User)
            .join(User, Patient.patient_id == User.user_id)
            .where(User.user_id == patient_id)
        )


        row = result.first()

        if not row:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        patient, user = row

        return PatientResponse(
            userData=user,
            patient_number=patient.patient_number
        )

        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching patient by id: {e}")
        raise HTTPException(status_code=500, detail=str(e))