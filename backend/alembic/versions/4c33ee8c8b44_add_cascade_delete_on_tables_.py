"""add cascade delete on tables translation and example

Revision ID: 4c33ee8c8b44
Revises: 7684561b85ba
Create Date: 2026-07-03 21:26:38.029944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c33ee8c8b44'
down_revision: Union[str, Sequence[str], None] = '7684561b85ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint('translations_word_id_fkey', 'translations', type_="foreignkey")
    op.create_foreign_key(
        'translations_word_id_fkey',
        'translations',
        'words',
        ["word_id"],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_constraint('examples_word_id_fkey', 'examples', type_="foreignkey")
    op.create_foreign_key(
        'examples_word_id_fkey',
        'examples',
        'words',
        ["word_id"],
        ['id'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('translations_word_id_fkey', 'translations', type_="foreignkey")
    op.create_foreign_key(
        'translations_word_id_fkey',
        'translations',
        'words',
        ["word_id"],
        ['id'],
    )

    op.drop_constraint('examples_word_id_fkey', 'examples', type_="foreignkey")
    op.create_foreign_key(
        'examples_word_id_fkey',
        'examples',
        'words',
        ["word_id"],
        ['id'],
    )
