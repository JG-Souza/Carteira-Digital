"""Inicio

Revision ID: 2571aec330e9
Revises: 
Create Date: 2024-12-30 11:45:35.735534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2571aec330e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
