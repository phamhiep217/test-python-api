from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            return store.json()
        return {'message':'Store not found!'}, 404

    def post(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            return {'message':'Store is exist!'},400
        
        store = StoreModel(name)
        try:
            store.insert_to_db()
        except:
            {'message':'An Error occurred while creating the store!'},500  
        
        return store.json(),201

    def delete(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            try:
                store.delete_to_db()
            except:
                {'message':'An Error occurred while deleting the store!'},500
        
        return {'message':'Store deleted'}

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.find_all()]}