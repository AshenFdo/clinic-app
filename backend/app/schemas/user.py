
from pydantic import BaseModel, EmailStr,ConfigDict
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
    role: str

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

