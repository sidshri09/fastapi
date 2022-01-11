"""parent_post

Revision ID: 835f86a07fb6
Revises: 56a89318a3b5
Create Date: 2022-01-11 10:05:40.375901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '835f86a07fb6'
down_revision = '56a89318a3b5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('parent_post', sa.Integer(), nullable=True))
    pass


def downgrade():
    op.drop_column('posts','parent_post')
    pass
