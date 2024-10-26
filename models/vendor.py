from models import db
from models.event_vendor import event_vendor

class Vendor(db.Model):
    __tablename__ = 'Vendor'

    vendor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(45), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(512), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    service_fee = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Integer, nullable=True)

    # Relationship between Vendor and Review    
    reviews = db.relationship('Review', back_populates='vendor')
    
    # Relationship between Vendor and Event
    events = db.relationship('Event', secondary=event_vendor, back_populates='vendors')

    def serialize(self):
        return {
            'vendor_id': self.vendor_id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'image_path': self.image_path,
            'phone_number': self.phone_number,
            'email': self.email,
            'service_fee': self.service_fee,
        }
    
    def __repr__(self):
        return f'<Vendor {self.name}>'

    @property
    def star_rating(self):
        return self.rating if self.rating is not None else 0
