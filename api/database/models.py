import bleach
from sqlalchemy import Column, String, Integer, Float
from api import db


class Report(db.Model):
    """
    Report Model
    """
    __tablename__ = 'reports'

    # Auto-incrementing, unique primary key
    id = Column(Integer, primary_key=True)
    # name
    name = Column(String(80), unique=True, nullable=True)
    # lat
    lat = Column(Float(13), unique=False, nullable=True)
    # long
    long = Column(Float(13), unique=False, nullable=True)
    # description
    description = Column(String(250), unique=False, nullable=False)
    # event_type
    event_type = Column(String(100), unique=False, nullable=False)
    # image
    image = Column(String(100), unique=False, nullable=True)

    def __init__(self, name, lat, long, description, event_type, image, report_id=None):
        if name is not None:
            name = bleach.clean(name).strip()
            if name == '':
                name = 'Anonymous'

        if lat == '':
          lat = None

        if long == '':
          long = None

        if description == '':
          description = None

        if event_type == '':
          event_type = None

        if image == '':
          image = None

        self.name = name
        self.lat = lat
        self.long = long
        self.description = description
        self.event_type = event_type
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
