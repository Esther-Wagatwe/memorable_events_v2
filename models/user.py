from models import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    profile_picture = db.Column(db.String(512), nullable=True, default='default_profile.jpeg')
    
    # Relationship between User and Events
    events = db.relationship('Event', back_populates='owner', lazy='dynamic')
    
    # Relationship between User and Reviews
    reviews = db.relationship('Review', back_populates='user', lazy='dynamic')

    # Method to get the user ID
    def get_id(self):
        return self.user_id

    # Method to set the password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check the password hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def serialize(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
        }
    
    def __repr__(self):
        return f'<User {self.username}>'


