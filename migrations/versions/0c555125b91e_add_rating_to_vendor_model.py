"""Add rating to Vendor model

Revision ID: 0c555125b91e
Revises: 
Create Date: 2024-10-25 09:49:45.032899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c555125b91e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Vendor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Vendor', schema=None) as batch_op:
        batch_op.drop_column('rating')

    # ### end Alembic commands ###
