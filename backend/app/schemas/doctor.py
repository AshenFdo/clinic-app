
from pydantic import BaseModel
from app.schemas.user import UserRegisterRequest


class DoctorRegisterRequest(BaseModel):
    """
    - DoctorRegisterRequest model representing the data required for doctor registration.
    - This is the payload expected when a new doctor registers via /auth/register.
    """
    userData: UserRegisterRequest
    specialty: str
    professional_bio: str
    years_of_experience: int