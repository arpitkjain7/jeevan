"""appointment_table_update

Revision ID: 7712959ed517
Revises: 
Create Date: 2023-05-22 10:10:02.424295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7712959ed517"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        table_name="appointments",
        column=sa.Column("appointment_status", sa.String(100)),
        schema="lobster",
    )
    # op.add_column(
    #     table_name="appointments",
    #     column=sa.Column("appointment_type", sa.String(100)),
    #     schema="lobster",
    # )


def downgrade() -> None:
    op.drop_column("lobster.appointments", "appointment_status")
    op.drop_column("lobster.appointments", "appointment_type")
