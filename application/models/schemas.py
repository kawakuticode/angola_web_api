from marshmallow import fields

from application.application_factory import ma
from application.models.radio_station import Radio
from application.models.weather import WeatherNow, Forecast


class WeatherNowSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WeatherNow
        include_relationships = True
        load_instance = True
    forecast_week = fields.Nested('ForecastSchema', many=True, load=True)


class ForecastSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Forecast
        load_instance = True


class RadioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Radio
        load_instance = True
