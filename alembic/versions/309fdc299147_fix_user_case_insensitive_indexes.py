"""fix user case insensitive indexes

Revision ID: 309fdc299147
Revises: 007031bdad44
Create Date: 2026-11-12 23:10:38.503802

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "309fdc299147"
down_revision: str | Sequence[str] | None = "007031bdad44"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_index("ux_users_username_lower", table_name="users")
    op.drop_index("ux_users_email_lower", table_name="users")

    op.create_index(
        "ux_users_username_lower",
        "users",
        [sa.text("lower(username)")],
        unique=True,
    )

    op.create_index(
        "ux_users_email_lower",
        "users",
        [sa.text("lower(email)")],
        unique=True,
    )


def downgrade() -> None:
    raise NotImplementedError(
        "This migration fixes broken unique indexes. "
        "Downgrading would reintroduce the original bug."
    )
