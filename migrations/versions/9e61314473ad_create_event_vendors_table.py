"""create event vendors table

Revision ID: 9e61314473ad
Revises: 46fa14503e9b
Create Date: 2024-10-31 15:33:23.620994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e61314473ad'
down_revision = '46fa14503e9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event_vendors', schema=None) as batch_op:
        batch_op.alter_column('event_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('vendor_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.create_unique_constraint('uq_event_vendors', ['event_id', 'vendor_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event_vendors', schema=None) as batch_op:
        batch_op.drop_constraint('uq_event_vendors', type_='unique')
        batch_op.alter_column('vendor_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('event_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
