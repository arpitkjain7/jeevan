"""patientMedicalRecord_column_type

Revision ID: 64dca93c7cdb
Revises: 7712959ed517
Create Date: 2023-05-23 07:59:43.361813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "64dca93c7cdb"
down_revision = "7712959ed517"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column(
        table_name="patientMedicalRecord", schema="lobster", column_name="abdm_linked"
    )
    op.add_column(
        table_name="patientMedicalRecord",
        column=sa.Column("abdm_linked", sa.Boolean(1)),
        schema="lobster",
    )


def downgrade() -> None:
    op.drop_column(
        table_name="patientMedicalRecord", schema="lobster", column_name="abdm_linked"
    )
    op.add_column(
        table_name="patientMedicalRecord",
        schema="lobster",
        column=sa.Column("abdm_linked", sa.String(100)),
        type_=sa.String,
    )
