"""Add budget field to Event model

Revision ID: 6314bb54ccfe
Revises: 477643737aad
Create Date: 2024-10-28 13:15:51.768127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6314bb54ccfe'
down_revision = '477643737aad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('budget', sa.Float(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Event', schema=None) as batch_op:
        batch_op.drop_column('budget')

    # ### end Alembic commands ###
