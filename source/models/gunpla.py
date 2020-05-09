from db import db


class GunplaModel(db.Model):
    __tablename__ = 'gunplas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225))
    model = db.Column(db.String(80))
    serie = db.Column(db.String(100))
    grade = db.Column(db.String(20))
    scale = db.Column(db.String(20))
    price = db.Column(db.Float(precision=2))
    release_date = db.Column(db.DateTime())
    brand = db.Column(db.String(40))

    def __init__(self, name, model, serie, grade,
                 scale, price, release_date, brand):
        self.name = name
        self.model = model
        self.serie = serie
        self.grade = grade
        self.scale = scale
        self.price = price
        self.release_date = release_date
        self.brand = brand

    def json(self):
        return {
            'name': self.name,
            'model': self.model,
            'serie': self.serie,            
            'grade': self.grade,
            'scale': self.scale,
            'price': self.price,
            'release_date': self.release_date,
            'brand': self.brand
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

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
