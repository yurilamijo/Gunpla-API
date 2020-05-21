from db import db
from flask import Flask, jsonify
from flask_restful import Api

from jwt_config import jwt_init
from resources.gunpla import Gunpla, GunplaList
from resources.serie import Serie, SerieList
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh

app = Flask(__name__)
app.config.from_pyfile('config.py')
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt_init(app)

# User calls
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(User, '/user<int:user_id>')
# Gunpla calls
api.add_resource(Gunpla, '/gunpla/<string:name>')
api.add_resource(GunplaList, '/gunplas')
# Serie calls
api.add_resource(Serie, '/serie/<string:name>')
api.add_resource(SerieList, '/series')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)