import logging

from supabase import create_client, Client
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import Awaitable, Callable
import uuid
from fastapi import HTTPException
from app.core.security import settings
from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schemas.user_auth import PatientAndAdminRegisterInput,UserRegisterResponse,UserResponse

logger = logging.getLogger(__name__)

def _build_user_metadata(data: PatientAndAdminRegisterInput) -> dict:
    """
    Formats user metadata for Supabase Auth based on the registration data and role.
    """
    return {
        "full_name": data.full_name,
        "email": data.email,
        "user_type": data.user_type,
        "gender": data.gender,
        "mobile_no": data.mobile_no,
        "date_of_birth": str(data.date_of_birth),
        "profile_image_url": data.profile_image_url or "",
    }

async def _add_patient_to_db(
    user_data: UserRegisterResponse,
    db: AsyncSession,
) -> User:
    """
    Add the user and its patient profile to the current transaction.
    """
    # Generate a patient number based on the user_id
    patient_number = f"PAT-{str(user_data.user_id)[:8].upper()}"

    # Check if the user and patient profile already exists in the database
    existing_user = await db.scalar(
        select(User).where(User.user_id == user_data.user_id)
    )
    if existing_user is not None:
        existing_patient = await db.scalar(
            select(Patient).where(Patient.patient_id == user_data.user_id)
        )
        # If the user exists but the patient profile does not, raise an error
        if existing_patient is None:
            raise HTTPException(
                status_code=409,
                detail="User exists but patient profile does not. Please contact support.",
            )

        return {
            "message": "User and patient profile already exist",
            "user": existing_user,
            "patient": existing_patient,
        }

    # Check if a user with the same email already exists in the database
    existing_user_by_email = await db.scalar(
        select(User).where(User.email == str(user_data.email))
    )
    if existing_user_by_email is not None:
        raise HTTPException(
            status_code=409,
            detail="A local account already exists for this email",
        )

    # Create a new User
    new_user = User(
        user_id=user_data.user_id,
        full_name=user_data.full_name,
        email=str(user_data.email),
        gender=user_data.gender,
        mobile_no=user_data.mobile_no,
        profile_image_url=user_data.profile_image_url or "",
        date_of_birth=user_data.date_of_birth,
        user_type=user_data.user_type,
        is_active=user_data.is_active,
        is_guest=False,
    )
    # Create a new Patient profile
    new_patient = Patient(
        patient_id=user_data.user_id,
        patient_number=patient_number,
    )

    # Add the new user and patient profile to the database session
    db.add(new_user)
    db.add(new_patient)
    try:
        await db.flush()
    except IntegrityError as exc:
        await db.rollback()
        logger.exception("Could not persist verified Supabase user %s", user_data.user_id)
        constraint = str(getattr(exc.orig, "constraint_name", "") or "")
        if constraint in {"User_email_key", "User_pkey"}:
            raise HTTPException(
                status_code=409,
                detail="This account already exists locally. Verify the email or use the existing account.",
            ) from exc
        raise HTTPException(
            status_code=500,
            detail="The verified account could not be saved. Check the server logs for the database constraint.",
        ) from exc

    await db.commit()
    return {
        "message": "User and patient profile created successfully",
        "user": new_user,
        "patient": new_patient,
    }










