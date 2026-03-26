from sqlalchemy import String, Integer, Numeric, Column, Date,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from app.models.base import Base


class PrescriptionItem(Base):
    """
    Prescription_Item model representing the items in a prescription.
    Attributes:
        item_id (UUID): Unique identifier for the prescription item.
        medicine_id (UUID): Identifier for the medicine in the prescription.
        prescription_id (UUID): Identifier for the prescription to which the item belongs.
        dosage (String): Dosage of the medicine.
        frequency (String): Frequency of taking the medicine.
        duration (String): Duration of the treatment.
        notes (String): Additional notes about the prescription item.
    """
    __tablename__ = "PrescriptionItem"

    item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    medicine_id = Column(UUID(as_uuid=True), ForeignKey("Medicine.medicine_id"), nullable=False)
    prescription_id = Column(UUID(as_uuid=True), ForeignKey("Prescription.prescription_id"), nullable=False)
    dosage = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    duration = Column(String, nullable=False)
    notes = Column(String, nullable=True)

    # Relationships
    medicine = relationship("Medicine", back_populates="prescription_items")
    prescription = relationship("Prescription", back_populates="prescription_items")
