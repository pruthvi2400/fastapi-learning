"""remove course column

Revision ID: 4ae33c947f68
Revises: b7d882e96ec3
Create Date: 2026-10-13 12:11:47.804669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ae33c947f68'
down_revision: Union[str, Sequence[str], None] = 'b7d882e96ec3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.drop_column("students", "course")


def downgrade() -> None:
    op.add_column(
        "students",
        sa.Column("course", sa.VARCHAR(length=50), nullable=True)
    )
