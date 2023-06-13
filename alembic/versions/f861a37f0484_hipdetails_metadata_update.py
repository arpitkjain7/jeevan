"""hipDetails_metadata_update

Revision ID: f861a37f0484
Revises: 1ad09693ddb6
Create Date: 2023-06-11 17:20:46.801192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f861a37f0484"
down_revision = "1ad09693ddb6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        table_name="hipDetails",
        column=sa.Column("hip_metadata", sa.JSON()),
        schema="lobster",
    )


def downgrade() -> None:
    op.drop_column(
        table_name="hipDetails", schema="lobster", column_name="hip_metadata"
    )
