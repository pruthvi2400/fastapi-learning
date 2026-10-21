"""change city column length

Revision ID: cc8ba6dab7dd
Revises: df0f48e611b1
Create Date: 2026-10-13 12:26:48.212339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc8ba6dab7dd'
down_revision: Union[str, Sequence[str], None] = 'df0f48e611b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "students",
        "city",
        existing_type=sa.VARCHAR(),
        type_=sa.String(length=100),
        existing_nullable=True
    )


def downgrade() -> None:
    op.alter_column(
        "students",
        "city",
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(),
        existing_nullable=True
    )
