

from application.application_factory import db
from application.application_factory import ma


class WeatherNow(db.Model):
    __tablename__ = 'weather_now'

    id = db.Column(db.Integer, primary_key=True)
    city_name =  db.Column ( db.TEXT , index=True, nullable=False)
    time_of_day =  db.Column ( db.TEXT , index = True, nullable=False)
    temperature =  db.Column ( db.TEXT , index = True, nullable=False)
    description =  db.Column ( db.TEXT , index = True, nullable=False)
    preciptation =  db.Column ( db.TEXT , index = True, nullable=False)
    humidity =  db.Column ( db.TEXT , index = True, nullable=False)
    wind = db.Column(db.TEXT, index=True, nullable=False)
    week_weather = db.relationship("WeatherDay", backref=db.backref('WeatherNow'), lazy='joined')

    def __init__(self, city_name, time_of_day, temperature, description, preciptation, humidity, wind, week_weather):
        self.city_name = city_name
        self.time_of_day = time_of_day
        self.temperature = temperature
        self.description = description
        self.preciptation = preciptation
        self.humidity = humidity
        self.wind = wind
        self.week_weather = week_weather

    def __str__(self):
        return f"weather now (city_name:{self.city_name}, time_of_day:{self.time_of_day}, temperature:{self.temperature}ºC, description:{self.description}, preciptation:{self.preciptation}, humidity:{self.humidity}, wind:{self.wind}) , week_weather:{self.week_weather})"

    def __repr__(self):
        return f"weather now (city_name:{self.city_name}, time_of_day:{self.time_of_day}, temperature:{self.temperature}ºC, description:{self.description}, preciptation:{self.preciptation}, humidity:{self.humidity}, wind:{self.wind}, week_weather:{self.week_weather})"


class WeatherDay(db.Model):
    __tablename__ = 'weather_day'
    id = db.Column(db.Integer, primary_key=True)
    weather_id = db.Column(db.Integer, db.ForeignKey('weather_now.id', onupdate='CASCADE', ondelete='CASCADE'),
                           nullable=False)
    day_of_week = db.Column(db.TEXT, index=True, nullable=False)
    description = db.Column(db.TEXT, index=True, nullable=False)
    min_temperature = db.Column(db.TEXT, index=True, nullable=False)
    max_temperature = db.Column(db.TEXT, index=True, nullable=False)


    def __init__(self, day_of_week, description, min_temperature, max_temperature):
        self.day_of_week = day_of_week
        self.description = description
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature

    def __str__(self):
        return f"weather_day('{self.day_of_week}', '{self.description}', '{self.min_temperature} ºC', '{self.max_temperature}ºC')"

    def __repr__(self):
        return f"weather_day(day_of_week:{self.day_of_week},description:{self.description}, min_temperature:{self.min_temperature}ºC, max_temperature:{self.max_temperature}ºC)"

    def __hash__(self):
        return hash(self.day_of_week)

class WeatherNowSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WeatherNow
        include_relationships = True
        load_instance = True



class WeatherDaySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WeatherDay
        load_instance = True
