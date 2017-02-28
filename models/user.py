import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    # user _id because id is a python keyword

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(_self):
        db.session.add(self) # is really an upsert
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()
