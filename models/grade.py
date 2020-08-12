from typing import List
from config.db import db


class GradeModel(db.Model):
    __tablename__ = 'grades'

    code = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(225), nullable=False)
    scale = db.Column(db.String(225), nullable=False)

    gunplas = db.relationship('GunplaModel', lazy='dynamic')

    @classmethod
    def find_by_code(cls, code: str) -> 'GradeModel':
        return cls.query.filter_by(code=code).first()

    @classmethod
    def find_all(cls) -> List['GradeModel']:
        return cls.query.all()

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            return {'message': 'An error occured while creating the grade'}, 500
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception:
            return {'message': 'An error occured while deleting the grade'}, 500
