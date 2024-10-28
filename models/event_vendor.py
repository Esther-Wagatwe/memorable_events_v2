"""Association table module for event-vendor relationships.

This module defines the many-to-many relationship table between events and vendors.
The table allows events to have multiple vendors and vendors to be associated with
multiple events.

Table Columns:
    event_id (int): Foreign key to Event table, part of composite primary key
    vendor_id (int): Foreign key to Vendor table, part of composite primary key
"""
from models import db

event_vendor = db.Table('event_vendor',
    db.Column('event_id', db.Integer, db.ForeignKey('Event.event_id'), primary_key=True),
    db.Column('vendor_id', db.Integer, db.ForeignKey('Vendor.vendor_id'), primary_key=True)
)
