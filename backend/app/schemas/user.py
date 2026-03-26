
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date
from typing import Optional
from decimal import Decimal
from pydantic import field_validator


class UserCreateInput(BaseModel):
    full_name: str
    gender: str

class UserResponse(BaseModel):
    user_id: UUID
    full_name: str
    Email: EmailStr
    gender: Optional[str]
    mobile_no: str
    profile_image_url: Optional[str]
    date_of_birth: Optional[date]
    password: Optional[str]
    role: str 
    is_active: int

    @field_validator("mobile_no", mode="before")
    @classmethod
    def coerce_mobile_no(cls, value):
        if value is None:
            return ""
        if isinstance(value, Decimal):
            return format(value, "f").rstrip("0").rstrip(".") or "0"
        return str(value)

    class Config:
        from_attributes = True
