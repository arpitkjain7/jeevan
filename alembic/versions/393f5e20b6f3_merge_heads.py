"""merge Heads

Revision ID: 393f5e20b6f3
Revises: 5d57c82fc135, f861a37f0484
Create Date: 2023-06-13 18:00:20.518287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "393f5e20b6f3"
down_revision = ("5d57c82fc135", "f861a37f0484")
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
