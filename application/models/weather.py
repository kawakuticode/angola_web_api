
from marshmallow import fields

from application.application_factory import db
from application.application_factory import ma


class WeatherNow(db.Model):
    __tablename__ = 'weather_now'

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.TEXT, index=True, nullable=False)
    time_of_day = db.Column(db.TEXT, index=True, nullable=False)
    temperature = db.Column(db.TEXT, index=True, nullable=False)
    description = db.Column(db.TEXT, index=True, nullable=False)
    preciptation = db.Column(db.TEXT, index=True, nullable=False)
    humidity = db.Column(db.TEXT, index=True, nullable=False)
    wind = db.Column(db.TEXT, index=True, nullable=False)
    forecast_week = db.relationship("Forecast", backref=db.backref('WeatherNow', lazy='dynamic'), lazy='dynamic')

    def __init__(self, city_name, time_of_day, temperature, description, preciptation, humidity, wind, forecast_week):
        self.city_name = city_name
        self.time_of_day = time_of_day
        self.temperature = temperature
        self.description = description
        self.preciptation = preciptation
        self.humidity = humidity
        self.wind = wind
        self.forecast_week = forecast_week

    def __str__(self):
        return f"weather now (city_name:{self.city_name}, time_of_day:{self.time_of_day}, " \
               f"temperature:{self.temperature}ºC, description:{self.description}, " \
               f"preciptation:{self.preciptation}, humidity:{self.humidity}, " \
               f"wind:{self.wind}) , forecast_week:{self.forecast_week})"

    def __repr__(self):
        return f"weather now (city_name:{self.city_name}, time_of_day:{self.time_of_day}," \
               f" temperature:{self.temperature}ºC, description:{self.description}, " \
               f"preciptation:{self.preciptation}, humidity:{self.humidity}, wind:{self.wind}, " \
               f"forecast_week:{self.forecast_week})"


class Forecast(db.Model):
    __tablename__ = 'forecast'
    id = db.Column(db.Integer, primary_key=True)
    weather_id = db.Column(db.Integer, db.ForeignKey('weather_now.id', onupdate='CASCADE', ondelete='CASCADE'),
                           nullable=False)
    day = db.Column(db.TEXT, index=True, nullable=False)
    description = db.Column(db.TEXT, index=True, nullable=False)
    min_temperature = db.Column(db.TEXT, index=True, nullable=False)
    max_temperature = db.Column(db.TEXT, index=True, nullable=False)

    def __init__(self, day, description, min_temperature, max_temperature):
        self.day = day
        self.description = description
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature

    def __str__(self):
        return f"[day:{self.day_of_week},description:{self.description}, min_temperature:{self.min_temperature}ºC," \
               f" max_temperature:{self.max_temperature}ºC]"

    def __repr__(self):
        return f"[day:{self.day_of_week},description:{self.description}, min_temperature:{self.min_temperature}ºC," \
               f" max_temperature:{self.max_temperature}ºC]"


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
