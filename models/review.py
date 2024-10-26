from models import db
from datetime import datetime


class Review(db.Model):
    __tablename__ = 'Reviews'

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    vendor_id = db.Column(db.Integer, db.ForeignKey('Vendor.vendor_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)

    vendor = db.relationship('Vendor', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

    def serialize(self):
        return {
            'review_id': self.review_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'vendor_id': self.vendor_id,
            'user_id': self.user_id,
        }