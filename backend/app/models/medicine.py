from sqlalchemy import String, Integer, Numeric, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base
from sqlalchemy.orm import relationship

class Medicine(Base):
    """ 
    Medicine model representing the medicines available in the clinic.
    Attributes:
        medicine_id (UUID): Unique identifier for the medicine.
        name (String): Name of the medicine.
        category (String): Category of the medicine (e.g., Antibiotic, Painkiller, etc.).
        description (String): Description of the medicine.
        quantity (Numeric): Quantity of the medicine available in stock.
    """
    __tablename__ = "Medicine"

    medicine_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=False)
    quantity = Column(Numeric, nullable=False)
    is_active = Column(String, nullable=False, default="Active")

    # Relationships
    prescription_items = relationship("PrescriptionItem", back_populates="medicine")