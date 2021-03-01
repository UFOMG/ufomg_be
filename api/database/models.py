import bleach
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from api import db


class Report(db.Model):
    """
    Report Model
    """
    __tablename__ = 'reports'

    # Auto-incrementing, unique primary key
# Auto-incrementing, unique primary key
    id = Column(Integer, primary_key=True)
    # name
    name = Column(String(80), nullable=True)
    # lat
    lat = Column(Float(13), unique=False, nullable=False)
    # long
    long = Column(Float(13), unique=False, nullable=False)
    # description
    description = Column(String(250), unique=False, nullable=False)
    # event_type
    event_type = Column(String(100), unique=False, nullable=False)
    # image
    image = Column(String(100), nullable=True)
    # city
    city = Column(String(100), unique=False, nullable=False)
    # state
    state = Column(String(100), unique=False, nullable=False)
    # created_at timestamp
    created_at = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # one to many relationship with comments here
    comments = relationship('Comment', backref='report', cascade='all, delete-orphan')

    def __init__(self, name, lat, long, description, event_type, image, city, state, report_id=None, created_at=None):
        if name is not None:
            name = bleach.clean(name).strip()
            if name == '':
                name = 'Anonymous'

        if image == '':
          image = None
        if created_at is not None:
            self.created_at = created_at
        self.name = name
        self.lat = lat
        self.long = long
        self.description = description
        self.event_type = event_type
        self.city = city
        self.state = state
        self.image = image
        if report_id is not None:
            self.id = report_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Comment(db.Model):
    """
    Comment Model
    """
    __tablename__= 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    report_id = Column(Integer, ForeignKey('reports.id'), nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, text, report_id, comment_id=None):

        if text == '':
          text = None

        self.text = text
        self.report_id = report_id
        if comment_id is not None:
            self.id = comment_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
