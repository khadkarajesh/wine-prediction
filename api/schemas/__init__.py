from api.common import ma
from api.models.wine import Wine


class WineSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Wine
        dump_only = ('id',)
        load_instance = True
