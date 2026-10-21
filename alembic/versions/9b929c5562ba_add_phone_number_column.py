"""add phone number column

Revision ID: 9b929c5562ba
Revises: a0a6618dfc8e
Create Date: 2026-10-13 11:56:27.842302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b929c5562ba'
down_revision: Union[str, Sequence[str], None] = 'a0a6618dfc8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.add_column(
        "students",
        sa.Column("phone_number", sa.String(length=15), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("students", "phone_number")
