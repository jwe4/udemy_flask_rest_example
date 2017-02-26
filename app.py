from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList



app = Flask(__name__)

# turns off the flask sqlalchmy change tracking ...
# let sqlalchemy do it, so that it can save to the
# db when changes are made, sqlalchemy has its own tracke
# this is not turned off, it is more efficient than
# the flask version
app.config('SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'mysecretkey999'  # in real app want to hide this
api = Api(app)
jwt = JWT(app, authenticate, identity)

# jwt creates a new endpoint /auth
# auth endpoint returns a jwt token


api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1/student/Rolf
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

# when import a file python runs the file
# may have a problem if run something twice
# so the following if fixes this
if __name__ == '__main__':
    from db import db
    dp.init_app(app)
    app.run(port=5000, debug=True)
