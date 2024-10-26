from models import db

class Guest(db.Model):
    __tablename__ = 'Guest'

    guest_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(45), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('Event.event_id'), nullable=False)

    # Relationship between Guest and Event  
    event = db.relationship('Event', back_populates='guests')
    
    # Relationship between Guest and Invitation
    invitations = db.relationship('Invitation', back_populates='guest')

    def serialize(self):
        return {
            'guest_id': self.guest_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'status': self.status,
            'event_id': self.event_id,
        }
    
    def __repr__(self):
        return f'<Guest {self.name} (Status: {self.status})>'