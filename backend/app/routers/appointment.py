from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.dependencies import get_db, get_current_user, require_role
from app.schemas.appointment import (
                            CreateAppointmentRequest,
                            AppointmentResponse,
                            AppointmentDetailsResponse,
                            UpdateAppointmentRequest
                        )
from app.services.appointment_services import (create_appointment as create_appointment_service,
                                             get_appointment_details,
                                             get_all_appointment,
                                             get_doctor_appointments_by_id,
                                            get_patient_appointments_by_id,
                                            update_appointment,
                                            delete_appointment
                                             )
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

@router.get("/all", response_model=list[AppointmentDetailsResponse])
async def get_all_appointments_details(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("Admin", "Doctor", "Patient")),
):
    """
    API endpoint to retrieve details of all appointments.
    - Admin can access all appointments.
    - Doctor and Patient can access only their own appointments.
    - Steps:
        1. Call the appointment service to fetch all appointments.
        2. Return a role-filtered list of appointment details.
    """
    return await get_all_appointment(db, current_user)

# -----------------------------------
# API router to get appointment details by ID
# -----------------------------------
@router.get("/{appointment_id}", response_model=AppointmentDetailsResponse) #, dependencies=[Depends(require_role("Admin", "Patient"))]
async def get_appointment_details_by_id(
    appointment_id: UUID,
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
    return await get_appointment_details(db, str(appointment_id))


# -----------------------------------
# API router to get appointments for a doctor by doctor ID
# -----------------------------------
@router.get("/doctor/{doctor_id}", response_model=list[AppointmentDetailsResponse], dependencies=[Depends(require_role("Admin", "Doctor"))])
async def get_appointments_for_doctor(
    doctor_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    API endpoint to retrieve all appointments for a specific doctor by their ID.
    - Admin can access appointments for any doctor, while doctors can only access their own appointments.
    - Steps:
        1. Extract the doctor_id parameter from the URL.
        2. Call the appointment service to fetch and validate the doctor's appointments.
        3. Return a list of appointment details for the specified doctor.
    """
    return await get_doctor_appointments_by_id(db, doctor_id)


# -----------------------------------
# API router to get appointments for a patient by patient ID
# -----------------------------------
@router.get("/patient/{patient_id}", response_model=list[AppointmentDetailsResponse], dependencies=[Depends(require_role("Admin", "Patient"))])
async def get_appointments_for_patient(
    patient_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    API endpoint to retrieve all appointments for a specific patient by their ID.
    - Admin can access appointments for any patient, while patients can only access their own appointments.
    - Steps:
        1. Extract the patient_id parameter from the URL.
        2. Call the appointment service to fetch and validate the patient's appointments.
        3. Return a list of appointment details for the specified patient.
    """
    return await get_patient_appointments_by_id(db, patient_id)


# -----------------------------------
# API router to update an appointment by ID
# -----------------------------------
@router.patch("/{appointment_id}", response_model=AppointmentDetailsResponse, dependencies=[Depends(require_role("Admin", "Doctor"))])
async def update_appointment_by_id(
    appointment_id: str,
    update_request: UpdateAppointmentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    API endpoint to update an existing appointment by its ID.
    - Both Patients and Admins can update appointments, but patients can only update their own appointments.
    - Steps:
        1. Extract the appointment_id parameter from the URL and parse the update request body.
        2. Call the appointment service to validate the appointment's existence and ownership, then apply updates.
        3. Return the updated appointment details in the response.
    """
    return await update_appointment(db, str(appointment_id), update_request, current_user)


# -----------------------------------
# API router to delete an appointment by ID
# -----------------------------------
@router.delete("/{appointment_id}", dependencies=[Depends(require_role("Admin", "Doctor"))])
async def delete_appointment_by_id(
    appointment_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    API endpoint to delete an existing appointment by its ID.
    - Both Patients and Admins can delete appointments, but patients can only delete their own appointments.
    - Steps:
        1. Extract the appointment_id parameter from the URL.
        2. Call the appointment service to validate the appointment's existence and ownership, then perform deletion.
        3. Return a success message or appropriate response indicating the result of the deletion operation.
    """
    return await delete_appointment(db, str(appointment_id), current_user)