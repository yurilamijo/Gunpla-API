from typing import List

from config.db import db

class GunplaModel(db.Model):
    __tablename__ = 'gunplas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), nullable=False, unique=True)
    model = db.Column(db.String(80), nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    scale = db.Column(db.String(20), nullable=True)
    price = db.Column(db.Float(precision=2), nullable=False)
    release_date = db.Column(db.DateTime(), nullable=True)
    brand = db.Column(db.String(40), nullable=True)

    serie_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=False)
    serie = db.relationship('SerieModel')

    @classmethod
    def find_by_name(cls, name: str) -> "GunplaModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_model(cls, model: str) -> List["GunplaModel"]:
        return cls.query.filter_by(model=model).all()
    
    @classmethod
    def find_by_serie(cls, serie_id: int) -> List["GunplaModel"]:
        return cls.query.filter_by(serie_id=serie_id).all()

    @classmethod
    def find_all(cls) -> List["GunplaModel"]:
        return cls.query.all()

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            return {'message': 'An error occured while creating the gunpla'}, 500

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            return {'message': 'An error occured while deleting the gunpla'}, 500
