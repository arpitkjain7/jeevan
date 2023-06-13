"""docDetails_hipId_update

Revision ID: 1ad09693ddb6
Revises: f519cd6ed187
Create Date: 2023-06-11 17:01:01.764243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1ad09693ddb6"
down_revision = "f519cd6ed187"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # op.add_column(
    #     table_name="docDetails",
    #     column=sa.Column("hip_id", sa.String(100)),
    #     schema="lobster",
    # )
    pass


def downgrade() -> None:
    op.drop_column(table_name="docDetails", schema="lobster", column_name="hip_id")
