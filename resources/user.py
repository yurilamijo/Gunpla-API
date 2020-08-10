from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
# from werkzeug.security import safe_str_cmp
import bcrypt

from schemas.user import UserSchema
from models.user import UserModel
from config.blacklist import BLACKLIST

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()

        if UserModel.find_by_username(user_json["username"]):
            return {'message': 'A user with this username already exists'}, 400
        
        password = user_json["password"].encode("utf-8")
        user_json["password"] = bcrypt.hashpw(password, bcrypt.gensalt(rounds=10))

        user = user_schema.load(user_json)

        user.save_to_db()

        return {'message': 'User created succesfully'}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete()
        return {'message': 'User deleted'}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_data = user_schema.load(request.get_json())
        
        user = UserModel.find_by_username(user_data.username)

        password = user_data.password.encode("utf-8")
        db_password = user.password.encode("utf-8")

        if user and bcrypt.checkpw(password, db_password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid Credentials!'}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Successfully loged out'}


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
