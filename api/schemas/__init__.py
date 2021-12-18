from api.common import ma
from api.models.wine import Wine


class WineSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Wine
        dump_only = ('id', 'predicted_label',)
        ordered = True
        load_instance = True
