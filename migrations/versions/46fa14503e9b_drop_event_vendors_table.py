"""drop event vendors table

Revision ID: 46fa14503e9b
Revises: e021fdb3b090
Create Date: 2024-10-31 15:30:23.608378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46fa14503e9b'
down_revision = 'e021fdb3b090'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event_vendors',
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('vendor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['Event.event_id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['Vendor.vendor_id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event_vendors')
    # ### end Alembic commands ###