"""add student city

Revision ID: b7d882e96ec3
Revises: 9b929c5562ba
Create Date: 2026-10-13 12:04:23.531840

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7d882e96ec3'
down_revision: Union[str, Sequence[str], None] = '9b929c5562ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.add_column(
        "students",
        sa.Column("city", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("students", "city")
