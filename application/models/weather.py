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
    wind =  db.Column ( db.TEXT , index = True, nullable=False)

    def __init__(self, city_name, time_of_day, temperature, description, preciptation, humidity, wind, next_days):
        self.city_name = city_name
        self.time_of_day = time_of_day
        self.temperature = temperature
        self.description = description
        self.preciptation = preciptation
        self.humidity = humidity
        self.wind = wind
        self.next_days = next_days

    def __str__(self):
        return f"weather now (city_name:{self.city_name}, time_of_day:{self.time_of_day}, temperature:{self.temperature}ºC, description:{self.description}, preciptation:{self.preciptation}, humidity:{self.humidity}, wind:{self.wind}) , next_days:{self.next_days})"

    def __repr__(self):
        return f"weather now (city_name:{self.city_name}, time_of_day:{self.time_of_day}, temperature:{self.temperature}ºC, description:{self.description}, preciptation:{self.preciptation}, humidity:{self.humidity}, wind:{self.wind}, next_days:{self.next_days})"


class WeatherDay(db.Model):
    __tablename__ = 'weather_day'
    id = db.Column(db.Integer, primary_key=True)
    weather_id = db.Column(db.Integer, db.ForeignKey('weather_now.id', ondelete="CASCADE"), nullable=False)
    weather_now = db.relationship("WeatherNow",
                                  backref=db.backref("weather_now", cascade="all, delete-orphan", uselist=False),
                                  lazy='joined')
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
        return f"weather of day (day of week:{self.day_of_week}, description:{self.description}, min_temperature:{self.min_temperature}, max_temperature:{self.max_temperature})"

    def __repr__(self):
        return f"weather of day (day of week:{self.day_of_week}, description:{self.description}, min_temperature:{self.min_temperature}, max_temperature:{self.max_temperature})"


class WeatherNowSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WeatherNow
        load_instance = True

class WeatherDaySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WeatherDay
        load_instance = True