import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel




class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="this filed cannot be left blank!"
    )


    @jwt_required()
    def get(self, name):  # allows get
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return { 'message': 'Item not found' }, 404


    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists,".format(name)}, 400
            # 400 means bad request
        data=Item.parser.parse_args()
        new_item= ItemModel(name, data['price'])
        try:
            new_item.insert()
        except:
            # 500 server error, 400 for user error
            return {'message': 'An error occurred inserting the item.'}, 500

        return new_item.json(), 201  # shows created, 202 if will be created after a delay

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("delete from items where name = ?",(name,))
        connection.commit()
        connection.close()
        return { 'message': 'Item deleted'}


    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name,data['price'])
        if item:
            try:
                updated_item.update()
            except:
                return {"message": "An error occurred updating the item"}, 500
        else:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occurred inserting the item"}, 500
        return updated_item.json()


class ItemList(Resource):

    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        result = cursor.execute("select * from items")
        items = []
        for row in result:
            items.append( { 'name' :  row[0], 'price': row[1]})
        connection.close()
        return { 'items': items }
