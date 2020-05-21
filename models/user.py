from typing import Dict
from config.db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    # def __init__(self, username: str, password: str):
    #     self.username = username
    #     self.password = password

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            return {'message': 'An error occurred while creating the user'}, 500

    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            return {'message': 'An error occurred while deleting the user'}, 500

    @classmethod
    def find_by_username(cls, username) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id) -> "UserModel":
        return cls.query.filter_by(id=_id).first()