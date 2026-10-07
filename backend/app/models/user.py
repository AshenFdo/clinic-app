from sqlalchemy import Boolean, String, Integer, Numeric, Column, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.models.base import Base

class User(Base):
    '''
    Users: - 4 users of application (Admin, Doctor, Patient, Guests)

    Admin: - Admin can manage the application, users, and settings.
    Doctor: - Doctor can view and manage patient records and appointments.
    Patient: - Patient can view their own records and schedule appointments.
    Guests: - Guests feature is available only for non-registered users to explore the application (should be restricted).

    '''
    __tablename__ = "User"
    

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    gender = Column(String, nullable=False)
    mobile_no = Column(String, nullable=False)
    profile_image_url = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=False)
    user_type = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_guest = Column(Boolean, nullable=False, default=False) # Indicates if the user is a guest user
    guest_expires_at = Column(Date, nullable=True)  # Only applicable for guest users

    # Relationships
    doctor = relationship("Doctor", back_populates="user", uselist=False)
    patient = relationship("Patient", back_populates="user", uselist=False)