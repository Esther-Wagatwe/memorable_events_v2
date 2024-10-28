"""Update budget column defaults

Revision ID: 88ddeeed47c0
Revises: 6314bb54ccfe
Create Date: 2024-10-28 14:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '88ddeeed47c0'
down_revision = '6314bb54ccfe'
branch_labels = None
depends_on = None

def upgrade():
    # Drop temporary table if it exists to prevent conflicts
    op.execute('DROP TABLE IF EXISTS event_temp')
    
    # Create temporary table
    op.create_table('event_temp',
        sa.Column('event_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('location', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=4082), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('name', sa.String(length=45), nullable=False),
        sa.Column('status', sa.Enum('ACTIVE', 'CANCELLED', 'COMPLETED', name='eventstatus'), nullable=False),
        sa.Column('budget', sa.Float(), server_default='0.0', nullable=False),
        sa.Column('spent_budget', sa.Float(), server_default='0.0', nullable=False),
        sa.Column('expenses', sqlite.JSON(), server_default='{}', nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['User.user_id'], ),
        sa.PrimaryKeyConstraint('event_id')
    )

    # Insert data into temp table
    op.execute('''
        INSERT INTO event_temp (
            event_id, owner_id, location, description, date, name, status
        )
        SELECT 
            event_id, owner_id, location, description, date, name, status
        FROM "Event"
    ''')

    # Drop old Event table and rename event_temp
    op.drop_table('Event')
    op.rename_table('event_temp', 'Event')


def downgrade():
    # Create old table structure
    op.create_table('event_old',
        sa.Column('event_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('location', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=4082), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('name', sa.String(length=45), nullable=False),
        sa.Column('status', sa.Enum('ACTIVE', 'CANCELLED', 'COMPLETED', name='eventstatus'), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['User.user_id'], ),
        sa.PrimaryKeyConstraint('event_id')
    )

    # Copy data back
    op.execute('''
        INSERT INTO event_old (event_id, owner_id, location, description, date, name, status)
        SELECT event_id, owner_id, location, description, date, name, status
        FROM "Event"
    ''')
    
    # Drop new table
    op.drop_table('Event')
    
    # Rename old table back
    op.rename_table('event_old', 'Event')
