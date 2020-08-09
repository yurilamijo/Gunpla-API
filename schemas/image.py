from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage


# Custom field
class FileStorageField(fields.Field):
    default_error_messages = {
        'invalid': 'Not a valid image.'
    }

    def _deserialize(self, value, attrs, data, **kwargs) -> FileStorage:
        if value is None:
            return None
        
        if not isinstance(value, FileStorage):
            self.fail('invaild')

        return value


class ImageSchema(Schema):
    image = FileStorageField(required=True)