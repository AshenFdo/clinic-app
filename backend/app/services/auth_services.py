from supabase import create_client, Client
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import uuid
from fastapi import HTTPException
from app.core.security import settings
from app.models.user import User
from app.models.patient import Patient
from app.schemas.user import UserRegisterRequest ,LoginRequest ,VerifyOTPRequest

# Utility function to get Supabase admin client
def get_supabase_admin() -> Client:
    """Service key gives admin access — can create users without email confirmation."""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


# ---------------------------------------------------------------
# Functions for patient registration process
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
    - This is called after registration and also in idempotent cases where the user already exists.
    - If the Patient profile already exists, it does nothing.
    - Does NOT commit—caller must handle commit.
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


async def register_patient(data: UserRegisterRequest, db: AsyncSession) -> User:
    """
    Register a new patient user across Supabase Auth and local database.
    
    - Step 1:Check for existing user by email (guard against duplicates).
    - Step 1b: Create user in Supabase Auth, then request signup OTP resend.
    - Step 2: Write user metadata to local User table.
    - Step 3: Create a linked Patient row with unique patient number.
    
    Idempotent: If user or email already exists, will return existing record and retry Patient profile creation.
    """
    # Guard against duplicate registrations by email in local DB.
    existing_user_by_email = await db.scalar(
        select(User).where(User.email == data.email)
    )

    if existing_user_by_email:
        # Idempotent behavior: if user exists but is not active, re-trigger OTP email.
        if not existing_user_by_email.is_active:
            _try_resend_signup_otp(get_supabase_admin(), existing_user_by_email.email)
        await _ensure_patient_profile(db, existing_user_by_email.user_id)
        await db.commit()
        return existing_user_by_email

    supabase = get_supabase_admin()
    supabase_uid = None

    try:
        # --- Step 1: Create in Supabase Auth ---
        auth_response = supabase.auth.admin.create_user({
            "email": data.email,
            "password": data.password,
            "email_confirm": False,
            "user_metadata": {
                "full_name": data.full_name,
                "role": "Patient",
                "gender":data.gender,
                "mobile_no": data.mobile_no,
                "date_of_birth": str(data.date_of_birth),
                "profile_image_url": data.profile_image_url or "", 
            }
        })

        if not auth_response or not auth_response.user or not auth_response.user.id:
            raise ValueError("Unable to create user in Supabase Auth")

        # This UUID is the link between Supabase Auth and local DB.
        supabase_uid = uuid.UUID(str(auth_response.user.id))
        # Trigger OTP email for email verification
        _try_resend_signup_otp(supabase, data.email)

        # Idempotency guard if local row was already created in a previous attempt.
        existing_user_by_id = await db.scalar(
            select(User).where(User.user_id == supabase_uid)
        )
        if existing_user_by_id:
            await _ensure_patient_profile(db, existing_user_by_id.user_id)
            await db.commit()
            return existing_user_by_id

        # Write to User table ---
        new_user = User(
            user_id=supabase_uid,
            full_name=data.full_name,
            email=data.email,
            gender=data.gender,
            mobile_no=data.mobile_no,
            date_of_birth=data.date_of_birth,
            profile_image_url=data.profile_image_url,
            role="Patient",
            is_active=False,
        )
        db.add(new_user)

        # Create Patient row with patient number format: PAT-XXXXXXXX
        patient_number = f"PAT-{str(supabase_uid)[:8].upper()}"
        new_patient = Patient(
            patient_id=supabase_uid,
            patient_number=patient_number,
        )
        db.add(new_patient)

        await db.commit()
        await db.refresh(new_user)
        return new_user
    except IntegrityError as exc:
        await db.rollback()

        # If the record already exists, return the existing row instead of failing.
        if supabase_uid is not None:
            existing_user = await db.scalar(
                select(User).where(User.user_id == supabase_uid)
            )
            if existing_user:
                await _ensure_patient_profile(db, existing_user.user_id)
                await db.commit()
                return existing_user

        existing_by_email = await db.scalar(
            select(User).where(User.email == data.email)
        )
        if existing_by_email:
            await _ensure_patient_profile(db, existing_by_email.user_id)
            await db.commit()
            return existing_by_email

        raise ValueError("Account already exists. Please verify your email or log in.") from exc
    except Exception:
        await db.rollback()
        # Clean up the Supabase Auth user if local DB write failed
        if supabase_uid is not None:
            try:
                supabase.auth.admin.delete_user(str(supabase_uid))
            except Exception:
                pass  # Log this — needs manual cleanup
        raise


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