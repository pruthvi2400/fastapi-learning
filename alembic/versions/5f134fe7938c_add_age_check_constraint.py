"""add age check constraint

Revision ID: 5f134fe7938c
Revises: a63f66dd182c
Create Date: 2026-10-13 12:45:55.826055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f134fe7938c'
down_revision: Union[str, Sequence[str], None] = 'a63f66dd182c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.create_check_constraint(
    "check_student_age_nonnegative",
    "students",
    "age >= 0"
)


def downgrade() -> None:
    op.drop_constraint("check_student_age_nonnegative", "students", type_="check")
    pass
    # ### end Alembic commands ###
