from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from libs import image_helper
from schemas.image import ImageSchema

class ImageUpload(Resource):
    @jwt_required
    def post(self):
        pass