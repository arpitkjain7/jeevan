"""condition added

Revision ID: 1fb4338cfed5
Revises: 6e1858149292
Create Date: 2023-06-15 10:02:12.056952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1fb4338cfed5"
down_revision = "6e1858149292"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "condition",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "pmr_id", sa.String, sa.ForeignKey("lobster.patientMedicalRecord.id")
        ),
        sa.Column("condition", sa.String),
        sa.Column("start_date", sa.DateTime),
        sa.Column("status", sa.String),
        sa.Column("notes", sa.String),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
        schema="lobster",
    )


def downgrade() -> None:
    op.drop_table("condition", schema="lobster")
