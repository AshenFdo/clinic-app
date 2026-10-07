"""fix User updated_at default

Revision ID: 8f4d6c7a1b2e
Revises: 6ecbb44759e2
Create Date: 2026-10-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8f4d6c7a1b2e"
down_revision: Union[str, None] = "6ecbb44759e2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        'UPDATE "User" SET updated_at = COALESCE(updated_at, created_at, now()) '
        'WHERE updated_at IS NULL'
    )
    op.alter_column(
        "User",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "User",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=None,
        nullable=False,
    )
