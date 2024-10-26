from models import db
from datetime import date
from enum import Enum as PythonEnum
from sqlalchemy import Enum as SqlAlchemyEnum
from sqlalchemy.orm import relationship
from .vendor import event_vendor

# Enum for Event Status
class EventStatus(PythonEnum):
    ACTIVE = 'active'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'

# Event Model
class Event(db.Model):
    __tablename__ = 'Event'

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(4082), nullable=True)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    status = db.Column(SqlAlchemyEnum(EventStatus), default=EventStatus.ACTIVE)

    # Relationship between Event and User
    owner = relationship('User', back_populates='events')

    # Relationship between Event and Guest
    guests = relationship('Guest', back_populates='event')
    
    # Relationship between Event and Invitation
    invitations = relationship('Invitation', back_populates='event')
    
    # Relationship between Event and Task
    tasks = relationship('Task', back_populates='event')
    
    # Relationship between Event and Vendor
    vendors = relationship('Vendor', secondary=event_vendor, back_populates='events')

    def serialize(self):
        return {
            'event_id': self.event_id,
            'name': self.name,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'location': self.location,
            'owner_id': self.owner_id,
        }
    
    def __repr__(self):
        return f'<Event {self.name} on {self.date}>'