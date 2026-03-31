"""add base timestamps

Revision ID: 926a300d3228
Revises: 0e77998eeb82
Create Date: 2026-03-31 10:32:17.677200

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '926a300d3228'
down_revision: Union[str, None] = '0e77998eeb82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE \"Appointment\" ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT now()")
    op.execute("ALTER TABLE \"AvailableSlots\" ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT now()")
    op.execute("ALTER TABLE \"Doctor\" ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT now()")
    op.execute("ALTER TABLE \"MedicalHistory\" ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT now()")
    op.execute("ALTER TABLE \"Medicine\" ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT now()")
    op.execute("ALTER TABLE \"Patient\" ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT now()")
    op.execute("ALTER TABLE \"Patient\" ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT now()")
    op.execute("ALTER TABLE \"Prescription\" ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT now()")
    op.execute("ALTER TABLE \"PrescriptionItem\" ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT now()")
    op.execute("ALTER TABLE \"Room\" ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT now()")
    op.execute("ALTER TABLE \"Room\" ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT now()")
    op.execute("ALTER TABLE \"TimeSlot\" ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT now()")
    op.execute("ALTER TABLE \"TimeSlot\" ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT now()")


def downgrade() -> None:
    op.execute("ALTER TABLE \"TimeSlot\" DROP COLUMN IF EXISTS updated_at")
    op.execute("ALTER TABLE \"TimeSlot\" DROP COLUMN IF EXISTS created_at")
    op.execute("ALTER TABLE \"Room\" DROP COLUMN IF EXISTS updated_at")
    op.execute("ALTER TABLE \"Room\" DROP COLUMN IF EXISTS created_at")
    op.execute("ALTER TABLE \"PrescriptionItem\" DROP COLUMN IF EXISTS updated_at")
    op.execute("ALTER TABLE \"Prescription\" DROP COLUMN IF EXISTS updated_at")
    op.execute("ALTER TABLE \"Patient\" DROP COLUMN IF EXISTS updated_at")
    op.execute("ALTER TABLE \"Patient\" DROP COLUMN IF EXISTS created_at")
    op.execute("ALTER TABLE \"Medicine\" DROP COLUMN IF EXISTS updated_at")
    op.execute("ALTER TABLE \"MedicalHistory\" DROP COLUMN IF EXISTS updated_at")
    op.execute("ALTER TABLE \"Doctor\" DROP COLUMN IF EXISTS updated_at")
    op.execute("ALTER TABLE \"AvailableSlots\" DROP COLUMN IF EXISTS updated_at")
    op.execute("ALTER TABLE \"Appointment\" DROP COLUMN IF EXISTS updated_at")
