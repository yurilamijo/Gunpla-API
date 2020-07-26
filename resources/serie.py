from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
        jwt_optional, 
        jwt_required, 
        get_jwt_claims, 
        get_jwt_identity
    )

from schemas.serie import SerieSchema
from models.serie import SerieModel

serie_schema = SerieSchema()
serie_list_schema = SerieSchema(many=True)

class Serie(Resource):
    parser = reqparse.RequestParser()

    @classmethod
    def get(cls, name: str):
        serie = SerieModel.find_by_name(name)
        if serie:
            return serie_schema.dump(serie), 201
        return {'message': 'Serie not found'}, 404
    
    @classmethod
    def post(cls, name: str):
        if SerieModel.find_by_name(name):
            return {'message': f'An Serie with the name {name} already exists'}, 400
        
        serie_json = request.get_json()
        serie_json["name"] = name

        serie = serie_schema.load(serie_json)
        serie.add()

        return serie_schema.dump(serie), 201

    @classmethod
    @jwt_required
    def delete(cls, name:str):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401

        serie = SerieModel.find_by_name(name)
        if serie:
            serie.delete()
            return {'message': f'The serie {name} is deleted'}
        return {'message': f"The serie {name} doesn't exist"}

class SerieList(Resource):
    @classmethod
    @jwt_optional
    def get(cls):
        user_id = get_jwt_identity()
        series = serie_list_schema.dump(SerieModel.find_all())
        if user_id:
            return {'series': series}, 200
        return {
                'series': [serie['name'] for serie in series],
                'message': 'Log in to see more details'
            }, 200
