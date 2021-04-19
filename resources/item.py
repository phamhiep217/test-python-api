import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='The field cannot be left blank!'
    )
    parser.add_argument('store_id',
        type= int,
        required=True,
        help='The filed cannot be left blank!'
    )


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)

        if item:
            return item.json()

        return {'message': 'Item not found'},404


    def post(self, name):
        data = Item.parser.parse_args()
        item = ItemModel(name,**data)

        if ItemModel.find_item_by_name(name):
            return {"message":"This item already exists!"}

        try:
            item.insert_to_db()
        except:
            return {"message":"has an error occurred inserting the item!"},500

        return item.json(),201


    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_to_db()

        return {"message":"Item deleted"}
    

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)
        if item is None:
            item = ItemModel(name,**data)
        else:
            item.price = data['price']

        item.insert_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}

    
