import sqlite3
from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # items = db.relationship('ItemModel')
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self,name):
        self.name = name

    def json(self):
        pass
        # return { 'name': self.name,  'items': [ item.json() for item in self.items] }
        # need self.items.all() --- because the db.relationship has lazy='dynamic'
        return { 'name': self.name,  'items': [ item.json() for item in self.items.all()] }

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()
        # equivalent to select * from items where name = name LIMIT 1
        # followed by conversion to an

    def save_to_db(self):
        db.session.add(self) # is really an upsert
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return [ store.json() for store in cls.query.all()]
