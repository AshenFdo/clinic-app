from .appointment import Appointment
from .available_slots import AvailableSlots
from .doctor import Doctor
from .medi_history import MedicalHistory
from .medicine import Medicine
from .patient import Patient
from .prescription import Prescription
from .prescription_item import PrescriptionItem
from .timeslot import TimeSlot
from .user import User

__all__ = [
    "Appointment",
    "AvailableSlots",
    "Doctor",
    "MedicalHistory",
    "Medicine",
    "Patient",
    "Prescription",
    "PrescriptionItem",
    "TimeSlot",
    "User",
]