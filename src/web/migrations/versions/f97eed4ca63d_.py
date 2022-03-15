"""empty message

Revision ID: f97eed4ca63d
Revises: b00e7914948b
Create Date: 2022-03-15 18:27:07.348198

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f97eed4ca63d'
down_revision = 'b00e7914948b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('api_key_expiration_date', sa.Integer(), nullable=False))
    op.drop_column('users', '_api_key_expiration_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('_api_key_expiration_date', sa.INTEGER(), nullable=False))
    op.drop_column('users', 'api_key_expiration_date')
    # ### end Alembic commands ###
