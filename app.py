from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'pham217'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/Item/<string:name>')
api.add_resource(ItemList, '/Items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/Store/<string:name>')
api.add_resource(StoreList, '/Stores')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port = 3000, debug = True)

