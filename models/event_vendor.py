from models import db

event_vendor = db.Table('event_vendor',
    db.Column('event_id', db.Integer, db.ForeignKey('Event.event_id'), primary_key=True),
    db.Column('vendor_id', db.Integer, db.ForeignKey('Vendor.vendor_id'), primary_key=True)
)
