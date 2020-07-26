from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import send_file, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback
import os

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
        # user_id = get_jwt_identity()
        folder = "gunpals"
        try:
            image_path = image_helper.save_image(data["image"], folder=folder)
            basename = image_helper.get_basename(image_path)
            return {"message": f"Image {basename} uploaded"}, 201
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": f"Extension {extension} not allowed"}, 400

class Image(Resource):
    @jwt_required 
    def get(self, filename: str):
        """
        Returns the requested image if it exists
        """
        folder = "gunpals"
        if not image_helper.is_filename_safe(filename):
            return {"message":"Illegal filename"}, 400

        try:
            return send_file(image_helper.get_path(filename, folder=folder))
        except FileNotFoundError:
            return {"message":"Image not found"}, 404

    @jwt_required
    def delete(self, filename: str):
        """
        Deletes the requested image
        """        
        folder = "gunpals"
        if not image_helper.is_filename_safe(filename):
            return {"message":"Illegal filename"}, 400
        
        try:
            os.remove(image_helper.get_path(filename, folder=folder))
            return {"message":f"Image {filename} deleted"}, 200
        except FileNotFoundError:
            return {"message":"Image not found"}, 404
        except:
            traceback.print_exc();
            return {"message":"Internal server error"}