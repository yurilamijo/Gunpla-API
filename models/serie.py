from typing import List
from config.db import db


class SerieModel(db.Model):
    __tablename__ = 'series'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), nullable=False, unique=True)
    type = db.Column(db.String(20), nullable=False)
    premiered = db.Column(db.String(50), nullable=False)
    studio = db.Column(db.String(100), nullable=False)

    gunplas = db.relationship('GunplaModel', lazy='dynamic')

    @classmethod
    def find_by_name(cls, name: str) -> "SerieModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["SerieModel"]:
        return cls.query.all()
    
    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            return {'message': 'An error occured while creating the serie'}, 500
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception:
            return {'message': 'An error occured while deleting the serie'}, 500
