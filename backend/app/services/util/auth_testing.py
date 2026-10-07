import asyncio

from supabase import create_client, Client
from app.schemas.user import UserRegisterRequest, UserResponse, VerifyOTPRequest
from app.core.security import settings
from fastapi import HTTPException
from app.schemas.user_auth import PatientAndAdminRegisterInput, UserRegisterResponse, UserResponse

from pydantic import BaseModel, EmailStr

from app.models.user import User


def get_supabase_admin() -> Client:
    """Service key gives admin access — can create users without email confirmation."""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

def _build_user_metadata(data: UserRegisterRequest, user_type: str) -> dict:
    """
    Formats user metadata for Supabase Auth based on the registration data and role.
    """
    return {
        "full_name": data.full_name,
        "user_type": user_type,
        "gender": data.gender,
        "mobile_no": data.mobile_no,
        "date_of_birth": str(data.date_of_birth),
        "profile_image_url": data.profile_image_url or "",
    }
def signup(body: UserRegisterRequest):
    supabase = get_supabase_admin()
    try:
        supabase.auth.sign_up({
            "email": body.email,
            "password": body.password,
            "options": {
                "data": _build_user_metadata(body, "patient")
            }
        })
    except Exception as e:
        raise HTTPException(400, str(e))
    return {"message": "Verification code sent to your email"}





class VerifyIn(BaseModel):
    email: EmailStr
    token: str





    
async def verify_signup_otp(body: VerifyIn) -> str:
    """Verify a signup OTP without blocking FastAPI's event loop."""
    token = body.token.strip()
    if not token:
        raise ValueError("OTP is required")

    supabase = get_supabase_admin()
    try:
        # supabase-py exposes a synchronous client, so run the network call
        # in a worker thread rather than blocking the async request loop.
        response = await asyncio.to_thread(
            supabase.auth.verify_otp,
            {
                "email": str(body.email),
                "token": token,
                "type": "email",
            },
        )
    except Exception as exc:
        raise ValueError("Invalid or expired OTP") from exc

    if not response or not getattr(response, "user", None):
        raise ValueError("Invalid or expired OTP")

    session = getattr(response, "session", None)
    access_token = getattr(session, "access_token", None)
    user_data:PatientAndAdminRegisterInput = getattr(response, "user", None).user_metadata
    if not access_token:
        raise ValueError("Verification succeeded but no session was created")

    new_user = User(
        full_name=user_data.full_name,
        email=body.email,
        gender=user_data.gender,
        mobile_no=user_data.mobile_no,
        profile_image_url=user_data.profile_image_url or "",
        date_of_birth=user_data.date_of_birth,
        user_type="P",
        is_active=True,  # Mark the user as active after successful OTP verification
    )

    return access_token , user_data , new_user