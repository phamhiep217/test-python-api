from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, 
    get_jwt, 
    get_jwt_identity
)
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


    # @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)

        if item:
            return item.json()

        return {'message': 'Item not found'},404

    @jwt_required(fresh=True)
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

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims['is_admin']:
            return {"message":"You dont have permission access this file"}
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
    # @jwt_required(optional=True)
    # def get(self):
    #     user_id = get_jwt_identity()
    #     items = [item.json() for item in ItemModel.find_all()]
    #     if user_id:
    #         return {'items': items},200
    #     return {
    #         'items':[item['name'] for item in items],
    #         'message': 'Data available when you log in'
    #         },200
    
    def get(self):
        items = [item.json() for item in ItemModel.find_all()]
        return {'items': items},200

    
