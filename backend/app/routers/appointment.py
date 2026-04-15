from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, get_current_user, require_role
from app.schemas.appointment import (
                            CreateAppointmentRequest,
                            AppointmentResponse,
                            AppointmentDetailsResponse
                        )
from app.services.appointment_services import (create_appointment as create_appointment_service,
                                             get_appointment_details)
from app.models.user import User

router = APIRouter(prefix="/appointment", tags=["Appointments"])

# -----------------------------------
# API router to create a new appointment
# -----------------------------------
@router.post("/create", response_model=AppointmentDetailsResponse, dependencies=[Depends(require_role("Admin", "Patient"))])
async def make_appointment(
    appointment_request: CreateAppointmentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    API endpoint to create a new appointment.
    - Both Patients and Admins can create appointments.
    - Steps:
        1. Parse and validate the appointment request parameters.
        2. Call the appointment service to handle business logic (validation, duplicate check, creation).
        3. Return the created appointment details in the response.
    """
    return await create_appointment_service(db, appointment_request, current_user)

# -----------------------------------
# API router to get appointment details by ID
# -----------------------------------
@router.get("/{appointment_id}", response_model=AppointmentDetailsResponse, dependencies=[Depends(require_role("Admin", "Patient"))])
async def get_appointment_details_by_id(
    appointment_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    API endpoint to retrieve detailed information about an appointment by its ID.
    - Both Patients and Admins can access appointment details.
    - Steps:
        1. Extract the appointment_id parameter from the URL.
        2. Call the appointment service to fetch and validate the appointment details.
        3. Return the complete appointment information with doctor and patient details.
    """
    return await get_appointment_details(db, appointment_id)