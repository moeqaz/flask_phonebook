"""Add address table

Revision ID: 5507e2950a96
Revises: 
Create Date: 2022-10-26 21:28:16.936770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5507e2950a96'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=False),
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('phone_number', sa.String(length=15), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone_number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contact')
    # ### end Alembic commands ###
