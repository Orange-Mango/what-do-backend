from datetime import datetime

from . import db

association_table = db.Table(  # pylint:disable=C0103
    'association', db.Model.metadata,
    db.Column('activity_id', db.Integer, db.ForeignKey('activities.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, default=0)
    description = db.Column(db.String(150), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    changed = db.Column(db.DateTime, onupdate=datetime.utcnow)
    description = db.Column(db.String(150), nullable=False)
    tags = db.relationship(
        'Tag',
        secondary=association_table,
        back_populates='activities'
    )


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    changed = db.Column(db.DateTime, onupdate=datetime.utcnow)
    name = db.Column(db.String(20), nullable=False)
    activities = db.relationship(
        'Activity',
        secondary=association_table,
        back_populates='tags'
    )


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    changed = db.Column(db.DateTime, onupdate=datetime.utcnow)
    google_id = db.Column(db.String(24))
    name = db.Column(db.String(100))
