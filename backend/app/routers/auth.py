from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.models.user import User
from app.core.dependencies import get_current_user
from app.schemas.user import UserRegisterRequest, UserResponse, ResendOTPRequest, LoginRequest ,VerifyOTPRequest
from app.services.auth_services import register_patient, verify_otp, resend_signup_otp, login_user,logout_user

# Define the API router for authentication-related endpoints
router = APIRouter(prefix="/auth", tags=["auth"])

# -------------------------------
# Patient Registration API Endpoint
# -------------------------------
@router.post("/register-patient", response_model=UserResponse)
async def register(data: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    """Patient self-registration. Triggers signup OTP through Supabase Auth."""
    try:
        user = await register_patient(data, db)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# -------------------------------
# OTP Verification API Endpoint
# -------------------------------
@router.post("/verify-otp")
async def verify(data: VerifyOTPRequest, db: AsyncSession = Depends(get_db)):
    """Verify signup OTP and activate the local user account."""
    success = await verify_otp(data)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user = await db.scalar(select(User).where(User.email == data.email))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Keep local user state aligned with Supabase email verification.
    user.is_active = True
    await db.commit()
    return {"message": "Email verified. You can now log in."}

# -------------------------------
# Resend OTP API Endpoint
# -------------------------------
@router.post("/resend-otp")
async def resend_otp(data: ResendOTPRequest):
    """Resend signup OTP to the user's email."""
    try:
        await resend_signup_otp(data.email)
        return {"message": "OTP resent successfully."}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

# -------------------------------
# Login API Endpoint
# -------------------------------
@router.post("/login")
async def login(data: LoginRequest):
    """
    Optional server-side login endpoint.
    Returns a Supabase JWT access token for valid credentials.
    """
    try:
        token = await login_user(data=data)
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    

# -------------------------------
# Logout API Endpoint
# -------------------------------
@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout endpoint to revoke the user's session server-side.
    Client MUST also call supabase.auth.signOut() to clear the local token.
    """
    try:
        return await logout_user(current_user)
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Logout failed") from exc
    

