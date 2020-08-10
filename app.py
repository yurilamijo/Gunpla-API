from config.db import db
from flask import Flask, jsonify
from flask_restful import Api
from flask_migrate import Migrate
from marshmallow import ValidationError
from flask_uploads import configure_uploads, patch_request_class
from dotenv import load_dotenv

from config.ma import ma
from config.jwt_config import jwt_init
from resources.gunpla import Gunpla, GunplaList
from resources.serie import Serie, SerieList
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.image import ImageUpload, Image
from libs.image_helper import IMAGE_SET

app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object('development_config')
app.config.from_envvar('APPLICATION_SETTINGS')
patch_request_class(app, 10 * 1024 * 1024)  # 10MB max size upload
configure_uploads(app, IMAGE_SET)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt_init(app)
migrate = Migrate(app, db)

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
# Image calls
api.add_resource(ImageUpload, "/upload/image")
api.add_resource(Image, "/image/<string:filename>")

db.init_app(app)
if __name__ == '__main__':
    ma.init_app(app)
    app.run()
