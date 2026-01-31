"""baseline

Revision ID: 27bf62123c7f
Revises: 47bd16d120cf
Create Date: 2026-01-31 12:13:51.742186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27bf62123c7f'
down_revision: Union[str, Sequence[str], None] = '47bd16d120cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
