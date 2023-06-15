"""PMR columns updated

Revision ID: 6e1858149292
Revises: ec7f15417142
Create Date: 2023-06-14 18:27:18.840986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6e1858149292"
down_revision = "ec7f15417142"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("diagnosis", sa.Column("status", sa.String()), schema="lobster")
    op.add_column("diagnosis", sa.Column("notes", sa.String()), schema="lobster")
    op.add_column("medicines", sa.Column("dosage", sa.String()), schema="lobster")
    op.add_column(
        "medicines", sa.Column("duration_period", sa.String()), schema="lobster"
    )
    op.create_table(
        "symptoms",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "pmr_id", sa.String, sa.ForeignKey("lobster.patientMedicalRecord.id")
        ),
        sa.Column("symptom", sa.String),
        sa.Column("duration", sa.String),
        sa.Column("severity", sa.String),
        sa.Column("notes", sa.String),
        sa.Column("start_date", sa.String),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
        schema="lobster",
    )
    op.create_table(
        "currentMedicines",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "pmr_id", sa.String, sa.ForeignKey("lobster.patientMedicalRecord.id")
        ),
        sa.Column("medicine_name", sa.String),
        sa.Column("start_date", sa.DateTime),
        sa.Column("status", sa.String),
        sa.Column("notes", sa.String),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
        schema="lobster",
    )


def downgrade() -> None:
    op.drop_column("diagnosis", sa.Column("status", sa.String()), schema="lobster")
    op.drop_column("diagnosis", sa.Column("notes", sa.String()), schema="lobster")
    op.drop_column("medicines", sa.Column("dosage", sa.String()), schema="lobster")
    op.drop_column(
        "medicines", sa.Column("duration_period", sa.String()), schema="lobster"
    )
    op.drop_table("symptoms", schema="lobster")
    op.drop_table("currentMedicines", schema="lobster")
