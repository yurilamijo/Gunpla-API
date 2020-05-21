from flask_restful import Resource, reqparse
from flask_jwt_extended import (
        jwt_optional, 
        jwt_required, 
        get_jwt_claims, 
        get_jwt_identity
    )
from models.serie import SerieModel
from constant_msg import EMPTY, NOT_EMPTY

class Serie(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'type',
        type=str,
        required=True, 
        help=NOT_EMPTY.format('type')
    )

    parser.add_argument(
        'premiered',
        type=str,
        required=True, 
        help=NOT_EMPTY.format('premiered')
    )

    parser.add_argument(
        'studio',
        type=str,
        required=True, 
        help=NOT_EMPTY.format('studio')
    )

    @classmethod
    def get(cls, name: str):
        serie = SerieModel.find_by_name(name)
        if serie:
            return serie.json(), 201
        return {'message': 'Serie not found'}, 404
    
    @classmethod
    def post(cls, name: str):
        if SerieModel.find_by_name(name):
            return {'message': f'An Serie with the name {name} already exists'}, 400
        
        data = Serie.parser.parse_args()
        serie = SerieModel(name, **data)
        serie.add()

        return serie.json(), 201

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
        series = [serie.json() for serie in SerieModel.find_all()]
        if user_id:
            return {'series': series}, 200
        return {
                'series': [serie['name'] for serie in series],
                'message': 'Log in to see more details'
            }, 200
