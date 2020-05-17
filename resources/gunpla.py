from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.gunpla import GunplaModel


class Gunpla(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'model',
        help='This field cannot be empty',
        required=True,
        type=str
    )    
    parser.add_argument(
        'serie',
        help='This field cannot be empty',
        required=True,
        type=str
    )    
    parser.add_argument(
        'grade',
        help='This field cannot be empty',
        required=True,
        type=str
    )
    parser.add_argument(
        'scale',
        help='This can be empty',
        required=False,
        type=str
    )    
    parser.add_argument(
        'price',
        help='This field cannot be empty',
        required=True,
        type=float
    )
    parser.add_argument(
        'release_date',
        help='This can be empty',
        required=False,
        type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S')
    )    
    parser.add_argument(
        'brand',
        help='This can be empty',
        required=False,
        type=str
    )    

    def get(self, name):
        gunpla = GunplaModel.find_by_name(name)
        if gunpla:
            return gunpla.json(), 201
        return {'message': 'Gunpla not found'}, 404

    def post(self, name):
        if GunplaModel.find_by_name(name):
            return {'message': f'An Gunpla with the name {name} already exists'}, 400
        
        data = Gunpla.parser.parse_args()
        gunpla = GunplaModel(name, **data)
        gunpla.add()

        return gunpla.json(), 201

    def put(self, name):
        data = Gunpla.parser.parse_args()
        gunpla = GunplaModel.find_by_name(name)

        if data is None:
            gunpla = GunplaModel(name, **data)
        else:
            gunpla.model = data['model']
            gunpla.serie = data['serie']
            gunpla.grade = data['grade']
            gunpla.scale = data['scale']
            gunpla.price = data['price']
            gunpla.brand = data['brand']

        gunpla.add()
        return gunpla.json(), 201

    def delete(self, name):
        gunpla = GunplaModel.find_by_name(name)
        if gunpla:
            gunpla.delete()
            return {'message': f'Gunpla {name} deleted'}
        return {'message': f"An Gunpla with the name {name} doesn't exsits"}, 401

class GunplaList(Resource):
    @jwt_required()
    def get(self):
        return {'gunplas': [gunpla.json() for gunpla in GunplaModel.query.all()]}