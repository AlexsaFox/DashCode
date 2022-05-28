"""Add 'profile_picture_filename' field to 'users'

Revision ID: 42a15f79d8b2
Revises: a09b45570e26
Create Date: 2022-04-26 17:36:19.023103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42a15f79d8b2'
down_revision = 'a09b45570e26'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_picture_filename', sa.String(length=40), nullable=False, server_default='default.webp'))
    op.alter_column('users', 'profile_picture_filename', server_default=None)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'profile_picture_filename')
    # ### end Alembic commands ###