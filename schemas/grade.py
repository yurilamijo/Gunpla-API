from config.ma import ma

from models.gunpla import GradeModel
from models.gunpla import GunplaModel
from schemas.gunpla import GunplaSchema


class GradeSchema(ma.SQLAlchemyAutoSchema):
    gunplas = ma.Nested(GunplaSchema, many=True)

    class Meta:
        model = GradeModel
        include_fk = True
        load_instance = True
