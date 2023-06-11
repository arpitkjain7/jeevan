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
        sa.Column("pmr_id", sa.String),
        sa.Column("diabetes_melitus", sa.String),
        sa.Column("hypertension", sa.String),
        sa.Column("hypothyroidism", sa.String),
        sa.Column("alcohol", sa.String),
        sa.Column("tobacco", sa.String),
        sa.Column("smoke", sa.String),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
    )


def downgrade() -> None:
    pass
