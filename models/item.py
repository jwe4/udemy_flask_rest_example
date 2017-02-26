import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self,name,price):
        self.name = name
        self.price = price

    def json(self):
        return { 'name': self.name,  'price': self.price }
        
    @classmethod
    def find_by_name(cls,name):
        return ItemModel.query.filter_by(name=name).first()
        # equivalent to select * from items where name = name LIMIT 1
        # followed by conversion to an

    def save_to_db(self):
        db.session.add(self) # is really an upsert
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()
