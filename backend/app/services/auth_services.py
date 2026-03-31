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
from app.schemas.user import UserRegisterRequest ,LoginRequest ,VerifyOTPRequest
from app.schemas.doctor import DoctorRegisterRequest

# Utility function to get Supabase admin client
def get_supabase_admin() -> Client:
    """Service key gives admin access — can create users without email confirmation."""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


# ---------------------------------------------------------------
# Functions for User registration process
# ---------------------------------------------------------------
def _try_resend_signup_otp(supabase: Client, email: str) -> None:
    """ 
    Internal: Attempt to resend signup OTP silently during registration.
    Used when user registers with existing unverified email or needs OTP retry.
    Silently swallows errors to avoid failing the registration flow.
    """
    try:
        supabase.auth.resend({
            "type": "signup",
            "email": email,
        })
    except Exception:
        # Avoid failing registration if resend is unavailable or SMTP is not configured.
        pass


async def _ensure_patient_profile(db: AsyncSession, user_id: uuid.UUID) -> None:
    """
    Ensure that a Patient profile exists for the given user_id.
    """
    existing_patient = await db.scalar(
        select(Patient).where(Patient.patient_id == user_id)
    )
    if existing_patient:
        return

    patient_number = f"PAT-{str(user_id)[:8].upper()}"
    db.add(
        Patient(
            patient_id=user_id,
            patient_number=patient_number,
        )
    )


async def _ensure_doctor_profile(
    db: AsyncSession,
    user_id: uuid.UUID,
    specialty: str,
    professional_bio: str,
    years_of_experience: int,
) -> None:
    """Ensure that a Doctor profile exists for the given user_id."""
    existing_doctor = await db.scalar(
        select(Doctor).where(Doctor.doctor_id == user_id)
    )
    if existing_doctor:
        return

    db.add(
        Doctor(
            doctor_id=user_id,
            specialty=specialty,
            professional_bio=professional_bio,
            years_of_experience=years_of_experience,
        )
    )


def _build_user_metadata(data: UserRegisterRequest, role: str) -> dict:
    """
    Formats user metadata for Supabase Auth based on the registration data and role.
    """
    return {
        "full_name": data.full_name,
        "role": role,
        "gender": data.gender,
        "mobile_no": data.mobile_no,
        "date_of_birth": str(data.date_of_birth),
        "profile_image_url": data.profile_image_url or "",
    }


async def _register_user_with_role(
    data: UserRegisterRequest,
    db: AsyncSession,
    role: str,
    ensure_profile: Callable[[AsyncSession, uuid.UUID], Awaitable[None]],
) -> User:
    """
    Shared user registration flow for both patients and doctors.
    - Checks for existing user by email and handles unverified accounts.
    - Creates user in Supabase Auth and local database.
    - Calls ensure_profile callback to create role-specific profile data.
    """

    # Validate if a user with the same email already exists in the local database
    existing_user_by_email = await db.scalar(
        select(User).where(User.email == data.email)
    )

    if existing_user_by_email:
        if not existing_user_by_email.is_active:
            _try_resend_signup_otp(get_supabase_admin(), existing_user_by_email.email)
        await ensure_profile(db, existing_user_by_email.user_id)
        await db.commit()
        return existing_user_by_email

    # Define supabase client and initialize variable to track created user ID for potential cleanup
    supabase = get_supabase_admin()
    supabase_uid = None

    try:
        # Create user in Supabase Auth with the provided email and password
        auth_response = supabase.auth.admin.create_user({
            "email": data.email,
            "password": data.password,
            "email_confirm": False,
            "user_metadata": _build_user_metadata(data, role),
        })

        # Validate that the user was created successfully in Supabase Auth and extract the user ID
        if not auth_response or not auth_response.user or not auth_response.user.id:
            raise ValueError("Unable to create user in Supabase Auth")

        supabase_uid = uuid.UUID(str(auth_response.user.id))
        # Send OTP email for email verification. Supabase does not automatically send OTP for admin-created users.
        _try_resend_signup_otp(supabase, data.email)

        
        existing_user_by_id = await db.scalar(
            select(User).where(User.user_id == supabase_uid)
        )
        if existing_user_by_id:
            await ensure_profile(db, existing_user_by_id.user_id)
            await db.commit()
            return existing_user_by_id

        # Add the new user to the local database with is_active=False until they verify their email
        new_user = User(
            user_id=supabase_uid,
            full_name=data.full_name,
            email=data.email,
            gender=data.gender,
            mobile_no=data.mobile_no,
            date_of_birth=data.date_of_birth,
            profile_image_url=data.profile_image_url,
            role=role,
            is_active=False,
        )
        db.add(new_user)
        await ensure_profile(db, supabase_uid)

        await db.commit()
        await db.refresh(new_user)
        return new_user
    except IntegrityError as exc:
        await db.rollback()

        if supabase_uid is not None:
            existing_user = await db.scalar(
                select(User).where(User.user_id == supabase_uid)
            )
            if existing_user:
                await ensure_profile(db, existing_user.user_id)
                await db.commit()
                return existing_user

        existing_by_email = await db.scalar(
            select(User).where(User.email == data.email)
        )
        if existing_by_email:
            await ensure_profile(db, existing_by_email.user_id)
            await db.commit()
            return existing_by_email

        raise ValueError("Account already exists. Please verify your email or log in.") from exc
    except Exception:
        await db.rollback()
        if supabase_uid is not None:
            try:
                supabase.auth.admin.delete_user(str(supabase_uid))
            except Exception:
                pass
        raise


async def register_patient(data: UserRegisterRequest, db: AsyncSession) -> User:
    """Register a patient by reusing the shared user registration flow."""
    return await _register_user_with_role(
        data=data,
        db=db,
        role="Patient",
        ensure_profile=_ensure_patient_profile,
    )


# ---------------------------------------------------------------
# Doctor registration (Admin-only)
# ---------------------------------------------------------------

async def register_doctor(data: DoctorRegisterRequest, db: AsyncSession) -> User:
    """Register a doctor by reusing the shared user registration flow."""
    async def ensure_doctor(db_session: AsyncSession, user_id: uuid.UUID) -> None:
        await _ensure_doctor_profile(
            db=db_session,
            user_id=user_id,
            specialty=data.specialty,
            professional_bio=data.professional_bio,
            years_of_experience=data.years_of_experience,
        )

    return await _register_user_with_role(
        data=data.userData,
        db=db,
        role="Doctor",
        ensure_profile=ensure_doctor,
    )


# ---------------------------------------------------------------
# Functions for OTP verification and resend
# ---------------------------------------------------------------
async def verify_otp(data: VerifyOTPRequest) -> bool:
    """
    - Verify the OTP submitted by the user after signup.
    - Calls Supabase Auth to validate the token sent to their email.
    - Returns True if verification succeeded, False otherwise.
    
    Note: Caller is responsible for updating local User.is_active after successful verification.
    """
    supabase = get_supabase_admin()
    try:
        response = supabase.auth.verify_otp({
            "email": data.email,
            "token": data.otp,
            "type": "signup"
        })
        return response.user is not None
    except Exception:
        return False


async def resend_signup_otp(email: str) -> bool:
    """
    - Public API: Resend OTP email for unverified users.
    - Called explicitly by frontend when user requests OTP retry.
    """
    supabase = get_supabase_admin()
    try:
        supabase.auth.resend({
            "type": "signup",
            "email": email,
        })
    except Exception as exc:
        error_text = str(exc).lower()
        if "email rate limit exceeded" in error_text or "rate limit" in error_text:
            raise ValueError("Too many OTP requests. Please wait before trying again.") from exc
        raise ValueError("Unable to resend OTP right now. Please try again.") from exc
    return True


# ---------------------------------------------------------------
# Functions for login/logout process
# ---------------------------------------------------------------
async def login_user(data: LoginRequest) -> str:
    """
    - Server-side login (optional). Client can also use Supabase JS SDK directly.
    - Returns JWT access token on successful login.
    """
    supabase = get_supabase_admin()

    try:
        response = supabase.auth.sign_in_with_password({"email": data.email, "password": data.password})
    except Exception as exc:
        error_text = str(exc).lower()
        if "email not confirmed" in error_text or "email not verified" in error_text:
            raise ValueError("Email is not verified. Please verify your email before login.") from exc
        if "invalid login credentials" in error_text or "invalid credentials" in error_text:
            raise ValueError("Invalid email or password") from exc
        raise ValueError("Login failed. Please try again.") from exc

    if not response.session or not response.session.access_token:
        raise ValueError("Invalid email or password")

    # Supabase marks verified emails with email_confirmed_at timestamp.
    if not getattr(response.user, "email_confirmed_at", None):
        raise ValueError("Email is not verified. Please verify your email before login.")

    return response.session.access_token

async def logout_user(current_user: User):
    """
    Revoke the user's session server-side.
    Client MUST also call supabase.auth.signOut() to clear the local token.
    """
    supabase = get_supabase_admin()
    try:
        # admin method — takes user_id, revokes all sessions for that user
        supabase.auth.admin.sign_out(str(current_user.user_id))
    except Exception:
        raise HTTPException(status_code=400, detail="Logout failed")

    return {"message": "Logged out successfully"}





# ---------------------------------------------------------------
# Admin Registration (not implemented yet)
# ---------------------------------------------------------------