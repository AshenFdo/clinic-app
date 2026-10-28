from pydantic import BaseModel, EmailStr, ConfigDict, model_validator
from uuid import UUID
from datetime import date
from typing import Literal, Optional
from decimal import Decimal
from pydantic import field_validator




class PatientAndAdminRegisterInput(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    gender: str
    mobile_no: str
    profile_image_url: Optional[str] = ""
    date_of_birth: date
    user_type: str = "patient"  # "patient" or "admin"

    
class UserRegisterResponse(BaseModel):
    user_id: UUID
    full_name: str
    email: EmailStr
    gender: str
    mobile_no: str
    profile_image_url: Optional[str] = ""
    date_of_birth: date
    user_type: str
    is_active: bool

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    full_name: str
    email: EmailStr
    gender: str
    mobile_no: str
    profile_image_url: Optional[str]
    date_of_birth: Optional[date]
    user_type: str
    sub: Optional[str] = None  # Optional field for Supabase user ID


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str


class ResendOTPRequest(BaseModel):
    email: EmailStr


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class GuestUserRequest(BaseModel):
    full_name: str
    gender: Literal["male", "female", "other"]
    age: int

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Full name is required")
        return value

    @field_validator("age")
    @classmethod
    def validate_age(cls, value: int) -> int:
        if value < 1 or value > 120:
            raise ValueError("Age must be between 1 and 120")
        return value