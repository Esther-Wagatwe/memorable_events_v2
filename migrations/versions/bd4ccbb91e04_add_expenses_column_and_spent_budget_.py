"""Add expenses column and spent_budget column to Event model

Revision ID: bd4ccbb91e04
Revises: 14cf46392af1
Create Date: 2024-10-26 13:09:22.342402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd4ccbb91e04'
down_revision = '14cf46392af1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('spent_budget', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('expenses', sa.JSON(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Event', schema=None) as batch_op:
        batch_op.drop_column('expenses')
        batch_op.drop_column('spent_budget')

    # ### end Alembic commands ###
