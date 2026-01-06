"""add content column to posts table

Revision ID: 6eda62a82718
Revises: 8f7adc46ff62
Create Date: 2026-01-05 17:03:12.769610

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6eda62a82718'
down_revision: Union[str, Sequence[str], None] = '8f7adc46ff62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
