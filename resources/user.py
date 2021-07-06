from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (create_access_token,
    create_refresh_token, 
    get_jwt_identity,
    jwt_required,
    get_jwt
)
from models.user import UserModel
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                            type= str,
                            required= True,
                            help= "This field cannot be blank!"
                            )
_user_parser.add_argument('password',
                            type= str,
                            required= True,
                            help= "This field cannot be blank!"
                            )

class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return {"message": "This user already exists!"},400
        user = UserModel(**data)
        user.insert_to_db() 

        return {"message": "User id created successfully."}

class User(Resource):
    
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':'User not found!'}, 404
        return user.json()
    
    classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':'User not found!'}, 404
        user.delete_to_db()
        return{'message':'Deleted!'}, 200

class UserLogin(Resource):
  
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            },200
        return {'message': 'Invalid credentials'}, 401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out.'}, 200

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token},200
 