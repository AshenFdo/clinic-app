from sqlalchemy import Boolean, String, Integer, Numeric, Column, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.models.base import Base

class User(Base):
    '''User model representing the users of the system.
    Attributes:
        user_id (UUID): Unique identifier for the user.
        full_name (String): Full name of the user.
        email (String): Email address of the user, must be unique.
        gender (String): Gender of the user.(Male, Female, Other)
        mobile_no (String): Mobile number of the user.
        profile_image_url (String): URL of the user's profile image.
        date_of_birth (Date): Date of birth of the user.
        password (String): Hashed password of the user.
        role (String): Role of the user (Admin, Doctor, Nurse, Patient).
        is_active (Boolean): Status of the user (True, False).
       
    '''
    __tablename__ = "User"
    

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    gender = Column(String, nullable=False)
    mobile_no = Column(String, nullable=False)
    profile_image_url = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    # Relationships
    doctor = relationship("Doctor", back_populates="user", uselist=False)
    patient = relationship("Patient", back_populates="user", uselist=False)