from config.ma import ma

from models.gunpla import GunplaModel
from models.serie import SerieModel


class GunplaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GunplaModel
        load_only = ('serie',)
        dump_only = ('id',)
        include_fk = True
        load_instance = True