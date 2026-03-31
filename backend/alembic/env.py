# alembic/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

# Import your Base and ALL models (every model must be imported here
# so Alembic can see them and detect changes)
from app.models.base import Base
from app.models.user import User
from app.models.appointment import Appointment
from app.models.available_slots import AvailableSlots
from app.models.doctor import Doctor
from app.models.medi_history import MedicalHistory
from app.models.medicine import Medicine
from app.models.patient import Patient
from app.models.prescription_item import PrescriptionItem
from app.models.prescription import Prescription
from app.models.room import Room
from app.models.timeslot import TimeSlot

# later you'll add: from app.models.doctor import Doctor  etc.

config = context.config

# Override the sqlalchemy.url with value from .env
config.set_main_option("sqlalchemy.url", os.getenv("SYNC_DATABASE_URL"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# This is what Alembic compares against your database to find differences
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()