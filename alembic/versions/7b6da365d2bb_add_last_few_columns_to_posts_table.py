"""add last few columns to posts table

Revision ID: 7b6da365d2bb
Revises: cdea3bb95a5f
Create Date: 2026-01-05 17:49:04.699955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b6da365d2bb'
down_revision: Union[str, Sequence[str], None] = 'cdea3bb95a5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column(
        'published',sa.Boolean(),nullable=False, server_default = 'TRUE'),)
    op.add_column('posts',sa.Column(
        'created_at',sa.TIMESTAMP(timezone=True), nullable = False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
