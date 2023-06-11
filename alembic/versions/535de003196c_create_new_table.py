"""Create new table

Revision ID: 535de003196c
Revises: bb824a8256d0
Create Date: 2023-06-11 14:50:08.193743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "535de003196c"
down_revision = "bb824a8256d0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "medicalHistory",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("pmr_id", sa.String, sa.ForeignKey("patientMedicalRecord.id")),
        sa.Column("diabetes_melitus", sa.String),
        sa.Column("hypertension", sa.String),
        sa.Column("hypothyroidism", sa.String),
        sa.Column("alcohol", sa.String),
        sa.Column("tobacco", sa.String),
        sa.Column("smoke", sa.String),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
    )
    op.add_column(
        table_name="patientMedicalRecord",
        column=sa.Column("oxygen_saturation", sa.Integer()),
        schema="lobster",
    )
    op.add_column(
        table_name="patientMedicalRecord",
        column=sa.Column("respiratory_rate", sa.Integer()),
        schema="lobster",
    )
    op.add_column(
        table_name="patientMedicalRecord",
        column=sa.Column("body_mass_index", sa.Integer()),
        schema="lobster",
    )
    op.add_column(
        table_name="patientMedicalRecord",
        column=sa.Column("systolic_blood_pressure", sa.Integer()),
        schema="lobster",
    )
    op.add_column(
        table_name="patientMedicalRecord",
        column=sa.Column("diastolic_blood_pressure", sa.Integer()),
        schema="lobster",
    )


def downgrade() -> None:
    pass
