import asyncio
import httpx
from supabase import create_client, Client
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import Awaitable, Callable
import uuid
from fastapi import HTTPException
from app.core.security import settings
from app.models.user import User
from app.schemas.user_auth import (
    PatientAndAdminRegisterInput,
    UserRegisterResponse,
    UserResponse,
    VerifyOTPRequest,
    UserLoginRequest,
    ResendOTPRequest,
    GuestUserResponse
)
from app.services.util.__auth import _build_user_metadata, _add_patient_to_db


# Get supabase client with service role key for admin access
def get_supabase_admin() -> Client:
    """Service key gives admin access — can create users without email confirmation."""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


# ============================
# User Signup function
# =================================
def user_signup(body: PatientAndAdminRegisterInput):
    """
    - Handles User signup by creating a new user in Supabase Auth
    - sending a verification code to the user's email.
    - "Path: /auth/register-patient", /auth/register-admin, /auth/register-doctor
    """
    try:
        supabase_client = get_supabase_admin()
        # Validate input data
        if not body.email or not body.password:
            raise HTTPException(status_code=400, detail="Email and password are required")

        # Validate user_type
        if body.user_type not in ["patient", "doctor", "admin"]:
            raise HTTPException(status_code=400, detail="Invalid user type")

        #Validate password Length
        if len(body.password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")

        # Create user in Supabase Auth
        response =  supabase_client.auth.sign_up({
            "email": body.email,
            "password": body.password,
            "options": {
                "data": _build_user_metadata(body)
            }
        })

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


    if response.user and not response.user.identities:
        raise HTTPException(status_code=400, detail="User already exists or email not confirmed")

    return {"message": "Verification code sent to your email", "user_metadata": response.user.user_metadata}


# ===========================
## Verify Signup OTP function
# ===========================
async def verify_signup_otp(data:VerifyOTPRequest, db: AsyncSession):
    """
    - Verifies the signup OTP sent to the user's email.
    - If the OTP is valid, it creates a new user in the local database.
    - Returns the newly created user and access token.
    - Path: /auth/verify-otp
    """
    token = data.otp.strip()
    if not token:
        raise ValueError("OTP is required")

    supabase = get_supabase_admin()
    try:
       response = await asyncio.to_thread(
                   supabase.auth.verify_otp,
                   {
                       "email": str(data.email),
                       "token": token,
                       "type": "email",
                   },
               )
    except Exception as exc:
        raise ValueError("Invalid or expired OTP") from exc
       
    if not response or not getattr(response, "user", None):
        raise ValueError("User not found or invalid OTP")


    session = getattr(response, "session", None)
    access_token = getattr(session, "access_token", None)
    user = getattr(response, "user", None)

    meta = user.user_metadata

    user_data:UserRegisterResponse = UserRegisterResponse(
        user_id= user.id,
        full_name=meta.get("full_name"),
        email=meta.get("email"),
        gender=meta.get("gender"),
        mobile_no=meta.get("mobile_no"),
        profile_image_url=meta.get("profile_image_url"),
        date_of_birth=meta.get("date_of_birth"),
        user_type=meta.get("user_type"),
        is_active=True,
    )
    if user_data.user_type == "patient":
        # Add the patient to the database
        new_user = await _add_patient_to_db(user_data, db)
    elif user_data.user_type == "admin":
        # Admin functionality can be added here if needed
        pass
    elif user_data.user_type == "doctor":
        # Doctor functionality can be added here if needed
        pass

    return new_user, access_token

# ============================
## Resend Signup OTP function
# ============================

def resend_signup_otp(data: ResendOTPRequest):
    """
    - Resends the signup OTP to the user's email.
    - Path: /auth/resend-otp
    """
    supabase = get_supabase_admin()

    try:
        supabase.auth.resend({
        "type":"signup",
        "email":data.email,
        })

        return {"message":"New otp sent to the email."}

    except HTTPException as e:
        error_text = str(e.detail) if hasattr(e, "detail") else str(e)
        if "email rate limit exceeded" in error_text or "rate limit" in error_text:
             raise ValueError("Too many OTP requests. Please wait before trying again.") from e
        raise ValueError("Unable to resend OTP right now. Please try again.") from e
    

# ===========================
# Login function
# ===========================
def user_login(data: UserLoginRequest):
    """
    - Handles User login by authenticating the user with Supabase Auth.
    - Returns the access token and user metadata if successful.
    - Path: /auth/login (applies for all user types: patient, doctor, admin)
    """
    supabase = get_supabase_admin()

    try:
        response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })

        if not response.user:
            raise ValueError("Invalid email or password")

        session = getattr(response, "session", None)
        access_token = getattr(session, "access_token", None)
        user_metadata = getattr(response.user, "user_metadata", None)

        return {"access_token": access_token, "user_metadata": user_metadata}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============================
# Refresh Token function
# ============================
def refresh_token(refresh_token: str):
    """
    - Handles token refresh by exchanging the refresh token for a new access token.
    """
    supabase = get_supabase_admin()

    try:
        response = supabase.auth.refresh_session(refresh_token)
        if not response.session:
            raise ValueError("Invalid refresh token")

        new_access_token = getattr(response.session, "access_token", None)
        return {"access_token": new_access_token}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============================
# Logout function
# ============================
async def user_logout(current_user: User, access_token: str):
    """
    - Handles User logout by revoking the current access token in Supabase Auth.
    - Path: /auth/logout
    """
    if not current_user or not current_user.user_id:
        raise HTTPException(status_code=401, detail="User is not authenticated")
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token is required")

    logout_url = f"{settings.SUPABASE_URL}/auth/v1/logout"
    headers = {
        "apikey": settings.SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {access_token}",
    }

    try:
        timeout = httpx.Timeout(connect=10.0, read=10.0, write=10.0, pool=10.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(logout_url, headers=headers)
        response.raise_for_status()
    except httpx.TimeoutException as exc:
        raise HTTPException(
            status_code=503,
            detail="Authentication provider timeout",
        ) from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=401 if exc.response.status_code == 401 else 502,
            detail="Could not log out from authentication provider",
        ) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=503,
            detail="Authentication provider unavailable",
        ) from exc

    return {"message": "User logged out successfully"}


# ===========================
# Create Guest User function
# ===========================
def create_guest_user(data: GuestUserResponse):
    """
    - Creates a guest user with the provided name, gender, and age.
    - Returns the guest user data.
    """
    try:
        supabase = get_supabase_admin()


        response = supabase.auth.sign_in_anonymously(
            {"options": {"data": data.model_dump()}}
        )
        session = getattr(response, "session", None)
        access_token = getattr(session, "access_token", None)
        if not access_token:
            raise ValueError("Failed to create guest user: no access token")

        user = getattr(response, "user", None)
        user_metadata = getattr(user, "user_metadata", None)
        return {
            "message": "Guest user created successfully",
            "access_token": access_token,
            "token_type": "bearer",
            "guest_user": {
                "user_id": getattr(user, "id", None),
                "metadata": user_metadata or data.model_dump(),
            },
        }


    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))