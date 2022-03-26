"""empty message

Revision ID: 42bb572d67f8
Revises: cacb1c13193e
Create Date: 2022-03-26 12:32:02.645517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42bb572d67f8'
down_revision = 'cacb1c13193e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('is_private', sa.Boolean(), nullable=False))
    op.drop_column('notes', 'private')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('private', sa.BOOLEAN(), nullable=False))
    op.drop_column('notes', 'is_private')
    # ### end Alembic commands ###
