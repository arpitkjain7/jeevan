"""appointmentTable_update

Revision ID: 57b414a3f505
Revises: 64dca93c7cdb
Create Date: 2023-05-29 23:20:43.072073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "57b414a3f505"
down_revision = "64dca93c7cdb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column(
        table_name="appointments", schema="lobster", column_name="appointment_date"
    )
    op.drop_column(
        table_name="appointments", schema="lobster", column_name="appointment_time"
    )
    op.add_column(
        table_name="appointments",
        column=sa.Column("slot_id", sa.Integer()),
        schema="lobster",
    )


def downgrade() -> None:
    op.drop_column(table_name="appointments", schema="lobster", column_name="slot_id")
    op.add_column(
        table_name="appointments",
        schema="lobster",
        column=sa.Column("appointment_time", sa.Date()),
    )
    op.add_column(
        table_name="appointments",
        schema="lobster",
        column=sa.Column("appointment_date", sa.Date()),
    )
