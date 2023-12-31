"""empty message

Revision ID: d27b6f7c770d
Revises: 
Create Date: 2023-11-26 20:26:51.656998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd27b6f7c770d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rent_date', sa.String(length=100), nullable=False),
    sa.Column('rent_place', sa.String(length=100), nullable=False),
    sa.Column('rent_time', sa.String(length=100), nullable=False),
    sa.Column('return_place', sa.String(length=100), nullable=False),
    sa.Column('return_time', sa.String(length=100), nullable=False),
    sa.Column('distance', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('member',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(length=100), nullable=False),
    sa.Column('login_id', sa.String(length=100), nullable=False),
    sa.Column('login_pw', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('member')
    op.drop_table('history')
    # ### end Alembic commands ###
