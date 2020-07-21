from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from libs import image_helper
from schemas.image import ImageSchema

image_schema = ImageSchema()

class ImageUpload(Resource):
    @jwt_required
    def post(self):
        """
        Used to upload an image (png, jpeg)
        """
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f"gunpals"
        try:
            image_path = image_helper.save_image(data["image"], folder=folder)
            basename = image_helper.get_basename(image_path)
            return {"message": f"Image {basename} uploaded"}, 201
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": f"Extension {extension} not allowed"}, 400
        