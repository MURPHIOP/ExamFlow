"""initial database schema

Revision ID: 20260508_0001
Revises:
Create Date: 2026-05-08 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op

from app.db.base import target_metadata

# revision identifiers, used by Alembic.
revision: str = "20260508_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    target_metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()
    target_metadata.drop_all(bind=bind)
