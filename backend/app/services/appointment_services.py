from app.schemas.appointment import CreateAppointmentRequest, AppointmentDetailsResponse, UpdateAppointmentRequest
from app.models.appointment import Appointment
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import select
from app.models.available_slots import AvailableSlots
from app.services.doctor_services import get_doctor_by_id
from app.services.patient_services import get_patient_by_id
from app.services.available_slots_services import get_available_slot_by_id
from app.schemas.doctor import DoctorResponse
from app.schemas.patient import PatientResponse
from app.schemas.available_slots import AvailableSlotsResponse


# -----------------------------------
# Helper functions to return AppointmentDetailsResponse
# -----------------------------------

async def _set_appointment_details_response(db: AsyncSession, appointment: Appointment) -> AppointmentDetailsResponse:
    """
    Helper function to construct an AppointmentDetailsResponse from an Appointment instance.
    - Fetches related doctor, patient, and available slot details to populate the response.
    - Formats the slot time as "start_time - end_time" for the response.
    - Returns an AppointmentDetailsResponse with all relevant information.
    """

    try:
        # Fetch related Doctor to get doctor details
        doctor_details: DoctorResponse = await get_doctor_by_id(db=db, doctor_id=str(appointment.doctor_id))
        if not doctor_details:
            raise HTTPException(status_code=404, detail="Doctor not found")

        # Fetch related Patient to get patient details
        patient_details: PatientResponse = await get_patient_by_id(str(appointment.patient_id), db)
        if not patient_details:
            raise HTTPException(status_code=404, detail="Patient not found")

        # Fetch related Available Slot to get slot details
        available_slot_details: AvailableSlotsResponse = await get_available_slot_by_id(db=db, as_id=str(appointment.as_id))
        if not available_slot_details:
            raise HTTPException(status_code=404, detail="Available slot not found")

        # Format the slot time as "start_time - end_time"
        slot_time = str(available_slot_details.start_time) + " - " + str(available_slot_details.end_time)

        # Return the appointment details along with doctor and patient information
        return AppointmentDetailsResponse(
            appointment_id=appointment.appointment_id,
            doctor_id=appointment.doctor_id,
            patient_id=appointment.patient_id,
            as_id=appointment.as_id,
            status=appointment.status,
            mode=appointment.mode,
            is_draft=appointment.is_draft,
            doctor_name=doctor_details.userData.full_name,
            patient_name=patient_details.userData.full_name,
            slot_time=slot_time,
            slot_date=available_slot_details.date,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(detail=str(e))




# -----------------------------------
# Function to create a new appointment
# -----------------------------------
async def create_appointment(db: AsyncSession, appointment_request: CreateAppointmentRequest, current_user: User):
    """
    Creates a new appointment in the database based on the provided request data.
    - Both Patients and Admins can create appointments.
    - Steps:
        1. Validate the current user exists.
        2. Validate the available slot exists and is valid for the doctor.
        3. Validate the doctor exists.
        4. Determine patient_id based on user role and request data:
            - If the user is a patient, they can only create appointments for themselves.
            - If the user is an admin, they must provide a patient_id in the request.
        5. Validate the patient exists.
        6. Fetch available slot details for formatting slot time.
        7. Check for duplicate appointments (same doctor, patient, and time slot).
        8. Create and save the appointment to the database.
    """
    try:
        # ---- Input Validation ----
        # Validate current user exists
        if not current_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Fetch available slot to ensure it exists and is valid for the doctor
        result = await db.execute(
            select(AvailableSlots)
            .where(AvailableSlots.as_id == appointment_request.as_id)
            .where(AvailableSlots.doctor_id == appointment_request.doctor_id)
            )
        av_slot = result.scalars().first()
        # Check if the available slot exists
        if not av_slot:
            raise HTTPException(status_code=404, detail="Available slot not found")

        # Fetch doctor to ensure it exists
        doctor = await get_doctor_by_id(db, av_slot.doctor_id or appointment_request.doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        # Determine patient_id based on user role and request data
        role = (current_user.role or "").strip().lower()
        if role == "patient":
            patient_id = appointment_request.patient_id or current_user.user_id
            if patient_id != current_user.user_id:
                raise HTTPException(status_code=403, detail="Patients can only create appointments for themselves")
        elif role == "admin":
            if not appointment_request.patient_id:
                raise HTTPException(status_code=400, detail="patient_id is required for admin-created appointments")
            patient_id = appointment_request.patient_id
        else:
            raise HTTPException(status_code=403, detail="Only Admin and Patient can create appointments")

        # Fetch patient to ensure it exists
        patient = await get_patient_by_id(str(patient_id), db)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        # Get slot details (reuse av_slot to avoid redundant query)
        available_slot_details: AvailableSlotsResponse = await get_available_slot_by_id(db=db, as_id=str(av_slot.as_id))
        if not available_slot_details:
            raise HTTPException(status_code=404, detail="Available slot not found")
        
        # Format the slot time as "start_time - end_time"
        slot_time = str(available_slot_details.start_time) + " - " + str(available_slot_details.end_time)

        # Check if an appointment already exists for the same doctor, patient, and time slot
        appointments_result = await db.execute(
            select(Appointment)
            .where(Appointment.as_id == appointment_request.as_id)
            .where(Appointment.doctor_id == appointment_request.doctor_id)
            .where(Appointment.patient_id == patient_id)
        )
        existing_appointment = appointments_result.scalars().first()
        # If an appointment already exists for the same doctor, patient, and time slot, raise an error
        if existing_appointment:
            raise HTTPException(status_code=400, detail="An appointment already exists for this doctor, patient, and time slot")


        # ---- Create and Save the Appointment ----

        # Create a new Appointment instance with the provided data
        new_appointment = Appointment(
            doctor_id=av_slot.doctor_id,
            patient_id=patient_id,
            as_id=av_slot.as_id,
            status=appointment_request.status,
            mode=appointment_request.mode,
            is_draft=False,
        )

        # Add the new appointment to the database session and commit the transaction
        db.add(new_appointment)
        await db.flush()
        await db.refresh(new_appointment)
        await db.commit()

        return AppointmentDetailsResponse(
            appointment_id=new_appointment.appointment_id,
            doctor_id=new_appointment.doctor_id,
            patient_id=new_appointment.patient_id,
            as_id=new_appointment.as_id,
            status=new_appointment.status,
            mode=new_appointment.mode,
            is_draft=new_appointment.is_draft,
            doctor_name=doctor.userData.full_name,
            patient_name=patient.userData.full_name,
            slot_time=slot_time,
            slot_date=available_slot_details.date,
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# -----------------------------------
# Function to get appointment details by ID
# -----------------------------------
async def get_appointment_details(db: AsyncSession, appointment_id: str):
    """
    Retrieves detailed information about an appointment.
    - Steps:
        1. Fetch the appointment by ID.
        2. Fetch related doctor details.
        3. Fetch related patient details.
        4. Fetch related available slot details.
        5. Format slot time and return complete appointment response.
    """
    try:
        # Fetch the appointment by ID
        row = await db.execute(
            select(Appointment)
            .where(Appointment.appointment_id == appointment_id)
        )
        # Get the first appointment from the result
        appointment = row.scalars().first()
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")

        # Use the helper function to construct the detailed response
        return await _set_appointment_details_response(db, appointment)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# -----------------------------------
# Function to get all appointments for a user
# -----------------------------------
async def get_all_appointment(db:AsyncSession, current_user:User):
    """
    Retrieves appointments based on the current user's role.
    - Admin: returns all appointments.
    - Patient: returns only appointments belonging to the current patient.
    - Doctor: returns only appointments belonging to the current doctor.
    - Raises a role-based access error for unsupported roles.
    """
    try:
        # Determine the user's role and fetch appointments accordingly
        user_role = (current_user.role or "").strip().lower()

        # Admin can access all appointments, while Patients and Doctors can only access their own appointments

        if user_role == "admin":
            results = await db.execute(select(Appointment))
            appointments = results.scalars().all()

            if not appointments:
                raise HTTPException(status_code=404, detail="Not found any appointments")

            appointment_responses = []

            for appointment in appointments:
                appointment_details = await _set_appointment_details_response(db, appointment)
                appointment_responses.append(appointment_details)

            return appointment_responses

        # if the user is a patient, they can only access their own appointments
        elif user_role == "patient":
            results = await db.execute(select(Appointment).where(Appointment.patient_id == current_user.user_id))
            appointments = results.scalars().all()

            if not appointments:
                raise HTTPException(status_code=404, detail="Not found any appointments for this patient")
            
            # return appointments for the current patient
            return await get_patient_appointments_by_id(db, str(current_user.user_id))
            
        # if the user is a doctor, they can only access their own appointments
        elif user_role == "doctor":
            results = await db.execute(select(Appointment).where(Appointment.doctor_id == current_user.user_id))
            appointments = results.scalars().all()

            if not appointments:
                raise HTTPException(status_code=404, detail="Not found any appointments for this doctor")
            
            # return appointments for the current doctor
            return await get_doctor_appointments_by_id(db, str(current_user.user_id))
            
        else:
            raise HTTPException(status_code=403, detail="Only Admin, Doctor and Patient can access appointments")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------
# Function to get all appointments for a doctor 
# -----------------------------------
async def get_doctor_appointments_by_id(db:AsyncSession, doctor_id:str):
    """
    Retrieves all appointments for a specific doctor.
    - Fetches appointments filtered by doctor_id.
    - Enriches each record with doctor, patient, and slot details.
    - Returns a list of AppointmentDetailsResponse.
    """
    try:
        results = await db.execute(
            select(Appointment)
            .where(Appointment.doctor_id == doctor_id)
        )
        appointments = results.scalars().all()

        appointment_responses = []
        
        for appointment in appointments:
            # Use the helper function to construct the detailed response for each appointment
            appointment_details = await _set_appointment_details_response(db, appointment)
            appointment_responses.append(appointment_details)

        return appointment_responses

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------------
# Function to get all appointments for a patient
# -----------------------------------
async def get_patient_appointments_by_id(db:AsyncSession, patient_id:str):
    """
    Retrieves all appointments for a specific patient.
    - Fetches appointments filtered by patient_id.
    - Enriches each record with doctor, patient, and slot details.
    - Returns a list of AppointmentDetailsResponse.
    """
    try:
        results = await db.execute(
            select(Appointment)
            .where(Appointment.patient_id == patient_id)
        )
        appointments = results.scalars().all()

        appointment_responses = []
        
        for appointment in appointments:
            # Use the helper function to construct the detailed response for each appointment
            appointment_details = await _set_appointment_details_response(db, appointment)
            appointment_responses.append(appointment_details)

        return appointment_responses

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# -----------------------------------
# Function to Update an appointment (Not implemented yet)
# -----------------------------------
async def update_appointment(db: AsyncSession, appointment_id: str, update_request: UpdateAppointmentRequest, current_user: User):
    """
    Updates an existing appointment in the database based on the provided request data.
    - Both Patients and Admins can update appointments.
    - Steps:
        1. Validate the current user exists.
        2. Fetch the appointment by ID and validate it exists.
        3. Check if the current user has permission to update this appointment (Admin can update any, Patients can only update their own).
        4. Update the appointment fields based on the request data.
        5. Save the changes to the database and return the updated appointment details.
    """
    try:
        current_user_role = (current_user.role or "").strip().lower()
        # Validate current user exists
        if not current_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if current_user_role not in ["admin", "doctor"]:
            raise HTTPException(status_code=403, detail="Only Admin and Doctor can update appointments")
        # Fetch the appointment by ID
        row = await db.execute(
            select(Appointment)
            .where(Appointment.appointment_id == appointment_id)
        )
        appointment = row.scalars().first()
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        update_data = update_request.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(appointment, key, value)


        await db.commit()
        await db.refresh(appointment)
        print(f"Updated appointment: {appointment}")
        return await _set_appointment_details_response(db, appointment)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------------
# Function to Delete an appointment 
# -----------------------------------
async def delete_appointment(db: AsyncSession, appointment_id: str, current_user: User):
    """
    Deletes an existing appointment from the database based on the provided appointment ID.
    - Both Patients and Admins can delete appointments.
    - Steps:
        1. Validate the current user exists.
        2. Fetch the appointment by ID and validate it exists.
        3. Check if the current user has permission to delete this appointment (Admin can delete any, Patients can only delete their own).
        4. Delete the appointment from the database and return a success message.
    """
    try:
        current_user_role = (current_user.role or "").strip().lower()
        # Validate current user exists
        if not current_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if current_user_role not in ["admin", "doctor", "patient"]:
            raise HTTPException(status_code=403, detail="Only Admin, Doctor, and Patient can delete appointments")
        # Fetch the appointment by ID
        row = await db.execute(
            select(Appointment)
            .where(Appointment.appointment_id == appointment_id)
        )
        appointment = row.scalars().first()
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        await db.delete(appointment)
        await db.commit()
        return {"detail": "Appointment deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))