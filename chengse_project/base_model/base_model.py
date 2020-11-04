from datetime import datetime

from chengse_project import db


class Base(db.Model):
    __abstract__ = True
    is_delete = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class BaseModel(Base):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
