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
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            # my solution to this is bad, leaves connection open

            query = "select * from users where username = ?"
            if UserModel.find_by_username(data['username']):
                return {"message": "user exists already"}, 400


            # null because id is auto-incremented
            query = "insert into users values(NULL, ?,?)"

            cursor.execute(query,(data['username'], data['password']))

            connection.commit()
            connection.close()

            return { "message": "User created success."}, 201
