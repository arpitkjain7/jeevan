"""appointment_type_default

Revision ID: 879ce23afbaa
Revises: 87451b49acf6
Create Date: 2023-06-20 09:34:37.880557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "879ce23afbaa"
down_revision = "87451b49acf6"
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
