"""add deployed_preprod_at and deployed_prod_at to releases

Revision ID: 5a8b9c1d2e3f
Revises: 4679a980ef5f
Create Date: 2025-10-21 17:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a8b9c1d2e3f'
down_revision: Union[str, Sequence[str], None] = '4679a980ef5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add deployed_preprod_at column
    op.add_column('releases', sa.Column('deployed_preprod_at', sa.DateTime(), nullable=True))
    # Add deployed_prod_at column
    op.add_column('releases', sa.Column('deployed_prod_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Drop deployed_prod_at column
    op.drop_column('releases', 'deployed_prod_at')
    # Drop deployed_preprod_at column
    op.drop_column('releases', 'deployed_preprod_at')
