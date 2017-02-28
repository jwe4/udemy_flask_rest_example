import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel



class UserRegister(Resource):
        parser = reqparse.RequestParser()
        parser.add_argument('username',
            type=str,
            required=True,
            help="this filed cannot be left blank!"
        )
        parser.add_argument('password',
            type=str,
            required=True,
            help="this filed cannot be left blank!"
        )
        def post(self):
            data=UserRegister.parser.parse_args()
            if UserModel.find_by_username(data['username']):
                return {"message": "user exists already"}, 400
            # user = UserModel(data['username'],data['password'])
            user = UserModel(**data) # same as above since data is a dictionary
            user.save_to_db()
            return { "message": "User created success."}, 201
