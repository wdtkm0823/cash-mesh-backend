"""update_categories_to_shared

Revision ID: 4be1019923a4
Revises: 4501d1e4d2a3
Create Date: 2025-10-23 23:44:39.583163

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4be1019923a4'
down_revision: Union[str, Sequence[str], None] = '4501d1e4d2a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # user_idカラムのForeign Key制約を削除
    op.drop_constraint('categories_user_id_fkey', 'categories', type_='foreignkey')

    # user_idインデックスを削除
    op.drop_index('ix_categories_user_id', table_name='categories')

    # user_idカラムを削除
    op.drop_column('categories', 'user_id')

    # nameカラムにUNIQUE制約を追加
    op.create_unique_constraint('uq_categories_name', 'categories', ['name'])


def downgrade() -> None:
    """Downgrade schema."""
    # UNIQUE制約を削除
    op.drop_constraint('uq_categories_name', 'categories', type_='unique')

    # user_idカラムを追加
    op.add_column('categories', sa.Column('user_id', sa.Integer(), nullable=False))

    # user_idインデックスを再作成
    op.create_index('ix_categories_user_id', 'categories', ['user_id'], unique=False)

    # Foreign Key制約を再作成
    op.create_foreign_key('categories_user_id_fkey', 'categories', 'users', ['user_id'], ['id'])
