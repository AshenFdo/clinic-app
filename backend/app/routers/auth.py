from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.core.dependencies import bearer_scheme
from app.models.user import User
from app.core.dependencies import get_current_user
from app.schemas.user_auth import (
    PatientAndAdminRegisterInput,
    UserRegisterResponse,
    UserResponse,
    VerifyOTPRequest,
    UserLoginRequest,
    ResendOTPRequest,
    GuestUserResponse
)
from app.services.auth_services import (
    user_signup, 
    verify_signup_otp,
    resend_signup_otp,
    user_login,
    user_logout,
    refresh_token,
    create_guest_user as create_guest_user_service,
)
router = APIRouter(prefix="/auth", tags=["auth"])

# ======================================
# Signup router
# =====================================

# Register patient  endpoint
@router.post("/register-patient") 
async def register_patient(data:PatientAndAdminRegisterInput):
    """Patient self-registration. Triggers signup OTP through Supabase Auth."""
    try:
        results = user_signup(data)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Register admin endpoint

# Register doctor endpoint

# ======================================
# Verify OTP router
# ======================================
@router.post("/verify-otp")
async def verify_otp(data: VerifyOTPRequest, db: AsyncSession = Depends(get_db)):
    """Verify the signup OTP sent to the user's email."""
    try:
        results = await verify_signup_otp(data, db)
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ======================================
# Resend OTP router
# ======================================
@router.post("/resend-otp")
async def resend_otp(data: ResendOTPRequest):
    """Resend the signup OTP to the user's email."""
    try:
        results = resend_signup_otp(data)
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ======================================
# User login router
# ======================================
@router.post("/login")
async def login(data: UserLoginRequest):
    """User login endpoint. apply for all user types (patient, doctor, admin)"""
    try:
        results = user_login(data)
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ======================================
# User logout router
# ======================================
@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: User = Depends(get_current_user),
):
    """User logout endpoint."""
    try:
        results = await user_logout(current_user, credentials.credentials)
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# =====================================
# Guest user creation router
# =====================================
@router.post("/create-guest-user")
async def create_guest_user(data: GuestUserResponse):
    try:
        results = create_guest_user_service(data)
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

