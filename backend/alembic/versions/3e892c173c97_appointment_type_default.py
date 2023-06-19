"""appointment_type_default

Revision ID: 3e892c173c97
Revises: 1fb4338cfed5
Create Date: 2023-06-16 09:28:55.401472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3e892c173c97"
down_revision = "1fb4338cfed5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        table_name="appointments",
        schema="lobster",
        column_name="appointment_type",
        server_default="consultation",
    )


def downgrade() -> None:
    op.alter_column(
        table_name="appointments",
        schema="lobster",
        column_name="appointment_type",
    )
