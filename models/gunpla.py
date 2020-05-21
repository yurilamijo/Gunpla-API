from typing import List, Dict
from db import db

class GunplaModel(db.Model):
    __tablename__ = 'gunplas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), unique=True)
    model = db.Column(db.String(80))
    grade = db.Column(db.String(20))
    scale = db.Column(db.String(20))
    price = db.Column(db.Float(precision=2))
    release_date = db.Column(db.DateTime())
    brand = db.Column(db.String(40))

    serie_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    serie = db.relationship('SerieModel')

    def __init__(self, name: str, model: str, serie_id: int, grade: str,
                 scale: str, price: float, release_date, brand: str):
        self.name = name
        self.model = model
        self.serie_id = serie_id
        self.grade = grade
        self.scale = scale
        self.price = price
        self.release_date = release_date
        self.brand = brand

    def json(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'serie_id': self.serie_id,         
            'serie': self.serie.name,         
            'grade': self.grade,
            'scale': self.scale,
            'price': self.price,
            'release_date': self.release_date,
            'brand': self.brand
        }

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
