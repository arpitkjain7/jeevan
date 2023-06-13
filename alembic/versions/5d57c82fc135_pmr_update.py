"""PMR update

Revision ID: 5d57c82fc135
Revises: 535de003196c
Create Date: 2023-06-12 14:03:22.247870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5d57c82fc135"
down_revision = "535de003196c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "vitals",
        sa.Column(
            "id",
            sa.Integer,
            primary_key=True,
            autoincrement=True,
        ),
        sa.Column("pmr_id", sa.String, sa.ForeignKey),
        sa.Column("height", sa.String),
        sa.Column("weight", sa.String),
        sa.Column("pulse", sa.String),
        sa.Column("blood_pressure", sa.String),
        sa.Column("body_temperature", sa.String),
        sa.Column("oxygen_saturation", sa.String),
        sa.Column("respiratory_rate", sa.String),
        sa.Column("body_mass_index", sa.String),
        sa.Column("systolic_blood_pressure", sa.String),
        sa.Column("diastolic_blood_pressure", sa.String),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
    )
    op.create_foreign_key(
        "fk_pmr_id",
        "vitals",
        "patientMedicalRecord",
        "pmr_id",
        "id",
    )
    op.drop_column(
        table_name="patientMedicalRecord", schema="lobster", column_name="height"
    )
    op.drop_column("patientMedicalRecord", "weight")
    op.drop_column("patientMedicalRecord", "pulse")
    op.drop_column("patientMedicalRecord", "blood_pressure")
    op.drop_column("patientMedicalRecord", "body_temperature")
    op.drop_column("patientMedicalRecord", "oxygen_saturation")
    op.drop_column("patientMedicalRecord", "respiratory_rate")
    op.drop_column("patientMedicalRecord", "body_mass_index")
    op.drop_column("patientMedicalRecord", "systolic_blood_pressure")
    op.drop_column("patientMedicalRecord", "diastolic_blood_pressure")


def downgrade() -> None:
    op.drop_table("vitals")
    op.drop_constraint("fk_pmr_id", "vitals", type_="foreignkey")
