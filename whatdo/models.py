from datetime import datetime

from . import app, db


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, default=0)
    description = db.Column(db.String(150), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    changed = db.Column(db.DateTime, onupdate=datetime.utcnow)
