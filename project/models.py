from .factory import db
from flask import current_app
from datetime import datetime
from sqlalchemy import orm
import secrets


class Analysis(db.Model):
    __tablename__ = 'analysises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(50))
    path = db.Column(db.String(128))
    link_hash = db.Column(db.String(30))
    status = db.Column(db.Integer)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)


    def __init__(self, **kwargs):
        super(Analysis, self).__init__(**kwargs)
        self.link_hash = secrets.token_hex(15)
        self.ping()
        self.status = 0 # not payed yet

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

