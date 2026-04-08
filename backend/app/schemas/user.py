
from pydantic import BaseModel, EmailStr, ConfigDict, model_validator
from uuid import UUID
from datetime import date
from typing import Optional
from decimal import Decimal
from pydantic import field_validator


class UserRegisterRequest(BaseModel):
    """
    - UserRegisterRequest model representing the data required for user registration.
    - This is the payload expected when a new user registers via /auth/register.
    """
    full_name: str
    email: EmailStr
    gender: str
    password: str
    mobile_no: str
    profile_image_url: Optional[str]
    date_of_birth: date

class LoginRequest(BaseModel):
    """
    LoginRequest model representing the data required for user login.
    """
    email: EmailStr
    password: str



class VerifyOTPRequest(BaseModel):
    """
    - VerifyOTPRequest model for verifying the OTP sent to user's email.
    - otp is the 6-digit OTP code from the email.
    """
    email: EmailStr
    otp: str   

class ResendOTPRequest(BaseModel):
    """
    - ResendOTPRequest model for requesting a new OTP to be sent to the user's email.
    """
    email: EmailStr


class ForgotPasswordRequest(BaseModel):
    """Request payload for sending password-reset OTP email."""
    email: EmailStr


class ResetPasswordWithOTPRequest(BaseModel):
    """Request payload for validating reset OTP and setting a new password."""
    email: EmailStr
    otp: str
    new_password: str
    confirm_password: str

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("New password and confirm password do not match")
        return self




class UserResponse(BaseModel):
    """
    UserResponse model representing the data returned in API responses about a user.
    """
    user_id: UUID
    full_name: str
    email: EmailStr
    gender: Optional[str]
    mobile_no: str
    profile_image_url: Optional[str]
    date_of_birth: Optional[date]
    role: str 

    # Enable parsing from ORM models
    model_config = ConfigDict(from_attributes=True) 

    @field_validator("mobile_no", mode="before")
    @classmethod
    def coerce_mobile_no(cls, value):
        """Convert mobile_no to string, handling Decimal from database."""
        if value is None:
            return ""
        if isinstance(value, Decimal):
            # Database may return numeric type; format as clean string without trailing zeros
            return format(value, "f").rstrip("0").rstrip(".") or "0"
        return str(value)
    

class UserUpdateRequest(BaseModel):
    """
    - UserUpdateRequest model representing the data allowed for updating a user's profile.
    - All fields are optional to allow partial updates.
    - Email & Password updates are not handled here.
    """
    full_name: Optional[str] = None
    gender: Optional[str] = None
    password: Optional[str] = None
    mobile_no: Optional[str] = None
    profile_image_url: Optional[str] = None
    date_of_birth: Optional[date] = None
