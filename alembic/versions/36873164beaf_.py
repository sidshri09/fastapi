"""empty message

Revision ID: 36873164beaf
Revises: b7408c01700b
Create Date: 2022-01-19 17:00:48.888882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36873164beaf'
down_revision = 'b7408c01700b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_pic', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'profile_pic')
    # ### end Alembic commands ###
