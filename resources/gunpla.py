from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
        jwt_required, 
        jwt_optional, 
        get_jwt_claims,
        get_jwt_identity, 
        fresh_jwt_required
    )
from marshmallow import ValidationError

from schemas.gunpla import GunplaSchema
from models.gunpla import GunplaModel
# from constant_msg import EMPTY, NOT_EMPTY

gunpla_schema = GunplaSchema()
gunpla_list_schema = GunplaSchema(many=True)

class Gunpla(Resource):
   
    @classmethod
    def get(cls, name: str):
        gunpla = GunplaModel.find_by_name(name)
        if gunpla:
            return gunpla_schema.dump(gunpla), 201
        return {'message': 'Gunpla not found'}, 404

    @classmethod
    def post(cls, name: str):
        if GunplaModel.find_by_name(name):
            return {'message': f'An Gunpla with the name {name} already exists'}, 400
        
        gunpla_json = request.json()
        gunpla_json['name'] = name

        try:
            gunpla = gunpla_schema.load(gunpla_json)
        except ValidationError as e:
            return e.messages, 400
        gunpla.add()

        return gunpla_schema.dump(gunpla), 201

    @classmethod
    def put(cls, name: str):
        gunpla_json = request.json()
        gunpla = GunplaModel.find_by_name(name)

        if gunpla is None:
            gunpla_json['name'] = name

            try:
                gunpla = gunpla_schema.load(gunpla_json)
            except ValidationError as e:
                return e.messages, 400
        else:
            gunpla.model = gunpla_json['model']
            gunpla.serie_id = gunpla_json['serie_id']
            gunpla.grade = gunpla_json['grade']
            gunpla.scale = gunpla_json['scale']
            gunpla.price = gunpla_json['price']
            gunpla.brand = gunpla_json['brand']

        gunpla.add()
        return gunpla_schema.dump(gunpla), 201

    @classmethod
    @jwt_required
    def delete(cls, name: str):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401

        gunpla = GunplaModel.find_by_name(name)
        if gunpla:
            gunpla.delete()
            return {'message': f'Gunpla {name} deleted'}
        return {'message': f"An Gunpla with the name {name} doesn't exsits"}, 401

class GunplaList(Resource):
    @classmethod
    @jwt_optional
    def get(cls):
        user_id = get_jwt_identity()
        gunplas = gunpla_list_schema.dump(GunplaModel.find_all())
        if user_id:
            return {'gunplas': gunplas}, 200
        return {
                'gunplas': [gunpla['name'] for gunpla in gunplas],
                'message': 'Log in to see more details'
            }, 200