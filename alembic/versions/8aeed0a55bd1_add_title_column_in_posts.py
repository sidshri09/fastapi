"""add title column in posts

Revision ID: 8aeed0a55bd1
Revises: 56a89318a3b5
Create Date: 2022-01-09 01:19:36.195510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8aeed0a55bd1'
down_revision = '56a89318a3b5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('title',sa.String(),nullable=True))
    pass


def downgrade():
    op.drop_column('posts','title')
    pass
