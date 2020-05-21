from typing import List, Dict
from db import db

class SerieModel(db.Model):
    __tablename__ = 'series'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), unique=True)
    type = db.Column(db.String(20))
    premiered = db.Column(db.String(50))
    studio = db.Column(db.String(100))

    gunplas = db.relationship('GunplaModel', lazy='dynamic')

    def __init__(self, name: str, type: str, premiered: str, studio: str):
        self.name = name
        self.type = type
        self.premiered = premiered
        self.studio = studio
    
    def json(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'premiered': self.premiered,
            'studio': self.studio,
            'gunplas': [gunpla.json() for gunpla in self.gunplas.all()]
        }

    @classmethod
    def find_by_name(cls, name: str) -> "SerieModel":
        return cls.query.filter_by(name=name).first()


    @classmethod 
    def find_all(cls) -> List["SerieModel"]:
        return cls.query.all()
    
    def add(self):
        try :
            db.session.add(self)
            db.session.commit()
        except:
            return {'message': 'An error occured while creating the serie'}, 500
    
    def delete(self):
        try :
            db.session.delete(self)
            db.session.commit()
        except:
            return {'message': 'An error occured while deleting the serie'}, 500
