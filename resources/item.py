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

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )


    @jwt_required()
    def get(self, name):  # allows get
        print("name is  {}".format(name))
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
        # new_item= ItemModel(name, data['price'], data['store_id'])
        new_item= ItemModel(name, **data)
        try:
            new_item.save_to_db()
        except:
            # 500 server error, 400 for user error
            return {'message': 'An error occurred inserting the item.'}, 500

        return new_item.json(), 201  # shows created, 202 if will be created after a delay

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return { 'message': 'Item deleted'}


    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            # item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()
        return item.json()


class ItemList(Resource):

    @jwt_required()
    def get(self):
        return { 'items' : ItemModel.find_all() }
