import os

from db import db
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.gunpla import Gunpla, GunplaList
from resources.user import UserRegister, User, UserLogin, TokenRefresh

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'yuri'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(User, '/user<int:user_id>')
api.add_resource(Gunpla, '/gunpla/<string:name>')
api.add_resource(GunplaList, '/gunplas')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)