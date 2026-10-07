from pydantic import BaseModel, EmailStr, ConfigDict, model_validator
from uuid import UUID
from datetime import date
from typing import Optional
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
    user_id: UUID
    full_name: str
    email: EmailStr
    gender: str
    mobile_no: str
    profile_image_url: Optional[str]
    date_of_birth: Optional[date]
    user_type: str
    sub: Optional[str]  # Optional field for Supabase user ID


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str


class ResendOTPRequest(BaseModel):
    email: EmailStr


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class GuestUserResponse(BaseModel):
    name : str
    gender : str
    age : int