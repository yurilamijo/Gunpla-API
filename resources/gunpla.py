from flask_restful import Resource, reqparse
from flask_jwt_extended import (
        jwt_required, 
        jwt_optional, 
        get_jwt_claims,
        get_jwt_identity, 
        fresh_jwt_required
    )

from models.gunpla import GunplaModel
from constant_msg import EMPTY, NOT_EMPTY

class Gunpla(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'model',
        help=NOT_EMPTY.format('model'),
        required=True,
        type=str
    )    
    parser.add_argument(
        'serie_id',
        help=NOT_EMPTY.format('serie_id'),
        required=True,
        type=int
    )    
    parser.add_argument(
        'grade',
        help=NOT_EMPTY.format('grade'),
        required=True,
        type=str
    )
    parser.add_argument(
        'scale',
        help=EMPTY.format('scale'),
        required=False,
        type=str
    )    
    parser.add_argument(
        'price',
        help=NOT_EMPTY.format('price'),
        required=True,
        type=float
    )
    parser.add_argument(
        'release_date',
        help=EMPTY.format('release_date'),
        required=False,
        type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S')
    )    
    parser.add_argument(
        'brand',
        help=EMPTY.format('brand'),
        required=False,
        type=str
    )    

    def get(self, name: str):
        gunpla = GunplaModel.find_by_name(name)
        if gunpla:
            return gunpla.json(), 201
        return {'message': 'Gunpla not found'}, 404

    def post(self, name: str):
        if GunplaModel.find_by_name(name):
            return {'message': f'An Gunpla with the name {name} already exists'}, 400
        
        data = Gunpla.parser.parse_args()
        gunpla = GunplaModel(name, **data)
        gunpla.add()

        return gunpla.json(), 201

    def put(self, name: str):
        data = Gunpla.parser.parse_args()
        gunpla = GunplaModel.find_by_name(name)

        if data is None:
            gunpla = GunplaModel(name, **data)
        else:
            gunpla.model = data['model']
            gunpla.serie_id = data['serie_id']
            gunpla.grade = data['grade']
            gunpla.scale = data['scale']
            gunpla.price = data['price']
            gunpla.brand = data['brand']

        gunpla.add()
        return gunpla.json(), 201

    @jwt_required
    def delete(self, name: str):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401

        gunpla = GunplaModel.find_by_name(name)
        if gunpla:
            gunpla.delete()
            return {'message': f'Gunpla {name} deleted'}
        return {'message': f"An Gunpla with the name {name} doesn't exsits"}, 401

class GunplaList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        gunplas = [gunpla.json() for gunpla in GunplaModel.find_all()]
        if user_id:
            return {'gunplas': gunplas}, 200
        return {
                'gunplas': [gunpla['name'] for gunpla in gunplas],
                'message': 'Log in to see more details'
            }, 200