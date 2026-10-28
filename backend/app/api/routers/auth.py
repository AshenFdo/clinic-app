import asyncio

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.dependencies import get_db
from ..core.dependencies import bearer_scheme
from ..models.user import User
from ..core.dependencies import get_current_user as get_current_user_dependency
from ..schemas.user_auth import (
    PatientAndAdminRegisterInput,
    UserRegisterResponse,
    UserResponse,
    VerifyOTPRequest,
    UserLoginRequest,
    ResendOTPRequest,
    GuestUserRequest,
    RefreshTokenRequest,
)
from ..services.auth_services import (
    user_signup, 
    verify_signup_otp,
    resend_signup_otp,
    user_login,
    user_logout,
    refresh_token,
    create_guest_user,
)
router = APIRouter(prefix="/auth", tags=["auth"])

# ======================================
# Signup router
# =====================================

# Register patient  endpoint
@router.post("/register")
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
        # supabase-py uses a synchronous HTTP client. Keep it off the
        # event loop so a slow provider request cannot block later logins.
        results = await asyncio.wait_for(
            asyncio.to_thread(user_login, data),
            timeout=30,
        )
        return results
    except asyncio.TimeoutError as exc:
        raise HTTPException(
            status_code=503,
            detail="Authentication provider timeout",
        ) from exc
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
):
    """User logout endpoint."""
    try:
        results = await user_logout(credentials.credentials)
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# =====================================
# Guest user creation router
# =====================================
@router.post("/create-guest-user")
async def create_guest_user_route(data: GuestUserRequest):
    try:
        # Call the service function to create a guest user
        results = create_guest_user(data)
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# =====================================
# Refresh token router
# =====================================
@router.post("/refresh-token")
async def refresh_token_route(
    data: RefreshTokenRequest,
):
    """Refresh the access token using the refresh token."""
    try:
        results = refresh_token(data.refresh_token)
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

 # =====================================
 # Get current user router
 # =====================================
@router.get("/current-user", response_model=UserResponse)
@router.get("/me", response_model=UserResponse, include_in_schema=False)
async def get_current_user_route(
    current_user: User = Depends(get_current_user_dependency),
):
    """Get the current logged-in user's information."""
    return current_user