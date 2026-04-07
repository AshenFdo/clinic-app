
from pydantic import BaseModel
from typing import Optional
from app.schemas.user import UserRegisterRequest ,UserResponse, UserUpdateRequest


class DoctorRegisterRequest(BaseModel):
    """
    - DoctorRegisterRequest model representing the data required for doctor registration.
    - This is the payload expected when a new doctor registers via /auth/register.
    """
    userData: UserRegisterRequest
    specialty: str
    professional_bio: str
    years_of_experience: int

class DoctorResponse(BaseModel):
    """
    DoctorResponse model representing the data returned in API responses about a doctor.
    """
    userData: UserResponse
    specialty: str
    professional_bio: str
    years_of_experience: int


class MockResponse(BaseModel):
    """
    MockResponse model representing a simple response with a message.
    This can be used for testing or placeholder responses.
    """
    message: str


class DoctorUpdateRequest(BaseModel):
    """
    DoctorUpdateRequest model representing the data required to update a doctor's profile.
    This can be used for updating doctor-specific fields as well as user-related fields.
    """
    userData: UserUpdateRequest
    specialty: Optional[str] = None
    professional_bio: Optional[str] = None
    years_of_experience: Optional[int] = None