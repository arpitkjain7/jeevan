"""hiu_consent_updates

Revision ID: 94e3520f0351
Revises: 4c9e95b1f65c
Create Date: 2023-06-22 09:27:26.599348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "94e3520f0351"
down_revision = "879ce23afbaa"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        table_name="hiu_consent",
        column=sa.Column("patient_data_raw", sa.JSON()),
        schema="lobster",
    )
    op.add_column(
        table_name="hiu_consent",
        column=sa.Column("patient_data_transformed", sa.JSON()),
        schema="lobster",
    )
    op.add_column(
        table_name="hiu_consent",
        column=sa.Column("requester_key_material", sa.JSON()),
        schema="lobster",
    )
    op.add_column(
        table_name="hiu_consent",
        column=sa.Column("transaction_id", sa.String(10)),
        schema="lobster",
    )


def downgrade() -> None:
    op.drop_column(
        table_name="hiu_consent", schema="lobster", column_name="transaction_id"
    )
    op.drop_column(
        table_name="hiu_consent", schema="lobster", column_name="requester_key_material"
    )

    op.drop_column(
        table_name="hiu_consent",
        schema="lobster",
        column_name="patient_data_transformed",
    )
    op.drop_column(
        table_name="hiu_consent",
        schema="lobster",
        column_name="patient_data_raw",
    )
