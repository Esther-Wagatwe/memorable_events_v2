from models import db

class Task(db.Model):
    __tablename__ = 'Task'

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='pending')
    event_id = db.Column(db.Integer, db.ForeignKey('Event.event_id'), nullable=False)
    due_date = db.Column(db.Date, nullable=False)

    # Relationship between Task and Event
    event = db.relationship('Event', back_populates='tasks')

    
    def serialize(self):
        return {
            'task_id': self.task_id,
            'description': self.description,
            'status': self.status,
            'event_id': self.event_id,
            'due_date': self.due_date.isoformat() if self.due_date else None,
        }
    
    def __repr__(self):
        return f'<Task {self.description} (Status: {self.status})>'