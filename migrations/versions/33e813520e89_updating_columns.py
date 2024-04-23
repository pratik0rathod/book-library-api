"""updating columns

Revision ID: 33e813520e89
Revises: 3f7e31e0437b
Create Date: 2024-04-23 10:16:31.914758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33e813520e89'
down_revision: Union[str, None] = '3f7e31e0437b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('books_created_by_fkey', 'books', type_='foreignkey')
    op.drop_column('books', 'created_by')
    op.alter_column('users', 'is_active',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('users', 'added_by_admin',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.drop_constraint('users_created_by_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'created_by')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('created_by', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_created_by_fkey', 'users', 'users', ['created_by'], ['id'])
    op.alter_column('users', 'added_by_admin',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('users', 'is_active',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.add_column('books', sa.Column('created_by', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('books_created_by_fkey', 'books', 'users', ['created_by'], ['id'])
    # ### end Alembic commands ###