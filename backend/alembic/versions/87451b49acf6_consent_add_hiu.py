"""consent_add_hiu

Revision ID: 87451b49acf6
Revises: f861a37f0484
Create Date: 2023-06-18 13:55:26.615991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "87451b49acf6"
down_revision = "f861a37f0484"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        table_name="consent",
        column=sa.Column("hiu_id", sa.String(100)),
        schema="lobster",
    )
    op.add_column(
        table_name="consent",
        column=sa.Column("hiu_name", sa.String(100)),
        schema="lobster",
    )


def downgrade() -> None:
    op.drop_column("lobster.consent", "hiu_name")
    op.drop_column("lobster.consent", "hiu_id")
