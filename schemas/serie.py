from config.ma import ma

from models.serie import SerieModel
from models.gunpla import GunplaModel
from schemas.gunpla import GunplaSchema

class SerieSchema(ma.SQLAlchemyAutoSchema):
    gunplas = ma.Nested(GunplaSchema, many=True)
    
    class Meta:
        model = SerieModel
        dump_only = ('id',)
        include_fk = True