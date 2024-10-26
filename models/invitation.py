from models import db

class Invitation(db.Model):
    __tablename__ = 'Invitation'

    invitation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(45), nullable=False, default='Pending')
    guest_id = db.Column(db.Integer, db.ForeignKey('Guest.guest_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('Event.event_id'), nullable=False)

    # Relationship between Invitation and Guest 
    guest = db.relationship('Guest', back_populates='invitations')
    
    # Relationship between Invitation and Event
    event = db.relationship('Event', back_populates='invitations')

    def serialize(self):
        return {
            'invitation_id': self.invitation_id,
            'status': self.status,
            'guest_id': self.guest_id,
            'event_id': self.event_id,
        }
    
    def __repr__(self):
        return f'<Invitation {self.invitation_id} (Status: {self.status})>'