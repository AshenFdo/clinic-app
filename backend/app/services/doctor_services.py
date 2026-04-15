
import inspect
from supabase import Client , create_client
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete
from app.models.doctor import Doctor 
from app.models.user import User
from app.schemas.doctor import DoctorUpdateRequest
from app.core.config import settings
from app.schemas.doctor import DoctorResponse

# --------------------------------
# Initialize Supabase client
# --------------------------------
def get_supabase_admin() -> Client:
    """Service key gives admin access — can create users without email confirmation."""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

# -----------------------------------
# Function to get all doctors
#  -----------------------------------
async def get_doctors(db:AsyncSession):
    """
    Fetches all doctors from the database, including their associated user data.
    """
    try:
        # Execute a query to fetch all doctors and their associated user data
        result = await db.execute(
            select(Doctor, User)
            .join(User, Doctor.doctor_id == User.user_id)
        )
        # Get all rows from the result
        rows = result.all()

        # Create a list of doctors with their user data and doctor-specific information

        return list[DoctorResponse](
            DoctorResponse(
                userData=user,
                specialty=doctor.specialty,
                professional_bio=doctor.professional_bio,
                years_of_experience=doctor.years_of_experience,
            )
            for doctor, user in rows
        )

    except Exception as e:
        print(f"Error in Fetching doctors {e}")
        raise HTTPException(status_code=500,detail=str(e))

# -----------------------------------
# Function to get doctor by id 
#  -----------------------------------
async def get_doctor_by_id(db:AsyncSession, doctor_id:str):
    """
    Fetches a doctor by their ID from the database, including their associated user data.
    """
    try:
        # Execute a query to fetch the doctor and associated user data based on the doctor_id
        result = await db.execute(
            select(Doctor,User)
            .join(User,Doctor.doctor_id == User.user_id)
            .where(Doctor.doctor_id == doctor_id)
        )
        # Get the first row from the result
        row = result.first()
        # If no doctor is found, raise a 404 HTTPException
        if not row:
            raise HTTPException(status_code=404, detail="Doctor not found") 
        
        # Unpack the doctor and user from the result row
        doctor, user = row

        return DoctorResponse(
            userData=user,
            specialty=doctor.specialty,
            professional_bio=doctor.professional_bio,
            years_of_experience=doctor.years_of_experience,
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# -----------------------------------
# Function to update doctor profile
#  -----------------------------------
async def update_doctor_data(db:AsyncSession,data: DoctorUpdateRequest, current_user:User ):
    """
    Updates a doctor's profile information in the database.
     - Fetches the doctor and associated user data based on the current user's ID.
     - Updates the doctor's specialty, professional bio, and years of experience if provided.
     - Updates the user's data if provided in the request.
     - Commits the changes to the database and returns the updated doctor information.
    """

    try:
        # Execute a query to fetch the doctor and associated user data based on the current user's ID
        result = await db.execute(
            select(Doctor,User)
            .where(Doctor.doctor_id == current_user.user_id)
            .join(User, Doctor.doctor_id == User.user_id)
        )

        # Get the first row from the result
        row = result.first()
        if row is None:
            raise HTTPException(status_code=404, detail="Doctor not found")

        # Extract the update data from the request, excluding unset fields
        update_data = data.model_dump(exclude_unset=True)
        
        # Unpack the doctor and user from the result row
        doctor,user = row

        # Extract user data from the update data, if provided
        user_data = update_data.pop("userData", {})

        # logic to update userData based on the provided update data
        for field, value in user_data.items():
            if value is  not None:
                setattr(user,field,value)

        # logic to update doctor specific data based on the provided update data
        for field, value in update_data.items():
            if value is not None:
                setattr(doctor, field, value)

        # Commit the changes to the database and refresh the user and doctor instances
        await db.commit()
        await db.refresh(user)
        await db.refresh(doctor)

        return DoctorResponse(
            userData=user,
            specialty=doctor.specialty,
            professional_bio=doctor.professional_bio,
            years_of_experience=doctor.years_of_experience,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    

# -----------------------------------
# Function to delete doctor profile
#  -----------------------------------
async def delete_doctor(db:AsyncSession,current_user:User):
    try:
        if (current_user.role or "").lower().strip() != "doctor" :
            raise HTTPException(status_code=403, detail="Only doctors can delete doctor profiles")

        supabase_admin = get_supabase_admin()
        user_id = str(current_user.user_id)

        stmt = delete(Doctor).where(Doctor.doctor_id == current_user.user_id)
        await db.execute(stmt)
        stmt = delete(User).where(User.user_id == current_user.user_id)
        await db.execute(stmt)
        delete_result = supabase_admin.auth.admin.delete_user(user_id)
        if inspect.isawaitable(delete_result):
            await delete_result

        await db.commit()
        return {"message": "Doctor profile deleted successfully"}

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500,detail=f"Delete doctor failed: {str(e)}")