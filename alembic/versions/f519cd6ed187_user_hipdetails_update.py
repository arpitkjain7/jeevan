"""user_hipDetails_update

Revision ID: f519cd6ed187
Revises: 57b414a3f505
Create Date: 2023-06-03 19:51:54.047851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f519cd6ed187"
down_revision = "57b414a3f505"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column(table_name="users", schema="lobster", column_name="hip_id")
    op.drop_column(table_name="users", schema="lobster", column_name="hip_name")
    op.add_column(
        table_name="users",
        column=sa.Column("hip_details", sa.JSON()),
        schema="lobster",
    )


def downgrade() -> None:
    op.drop_column(table_name="users", schema="lobster", column_name="hip_details")
    op.add_column(
        table_name="users", column=sa.Column("hip_id", sa.String(10)), schema="lobster"
    )
    op.add_column(
        table_name="users",
        column=sa.Column("hip_name", sa.String(10)),
        schema="lobster",
    )
