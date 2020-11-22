from flask import current_app as app
from flask import jsonify

from application.application_factory import db
from application.models.radio_station import Radio
from application.models.radio_station import RadioSchema
from application.models.weather import Forecast, ForecastSchema
from application.models.weather import WeatherNow, WeatherNowSchema
from application.utilities.weather_utilities import WeatherUtilities as weather_utilities

URL_WEATHER = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"

r_schema = RadioSchema()
rs_schema = RadioSchema(many=True)

wnow_schema = WeatherNowSchema()
wnows_schema = WeatherNowSchema(many=True)
week_schema = Forecast()
weeks_schema = ForecastSchema(many=True)


@app.before_first_request
def before_first_request_func():
    # W_uti.add_weather_now_db(db)
    # print("print called before first request")

    #    print("updating radios....")
    #   R_uti.update_radio_db(db)
    # W_uti.add_weather_now_db(db)
    weather_data = weather_utilities.get_weather_now(URL_WEATHER)
    if not weather_utilities.add_weather_now_db(weather_data, db):
        print("\n")
        print("updating weather now....")
        weather_utilities.update_weather_now_db(weather_data, db)


@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
@app.route("/index", methods=["GET"])
def home():
    return "welcome to angola web api!"


@app.route("/api/v1/radios", methods=["GET"])
def radios():
    radios_db = Radio.query.all()
    return jsonify(rs_schema.dump(radios_db)), 200


@app.route("/api/v1/radios/<string:radio_name>", methods=["GET"])
def get_radio_name(radio_name):
    radio_ = Radio.query.filter(Radio.r_name.ilike('%' + radio_name + '%')).first()
    if radio_ is None:
        response = {
            'message': 'this radio does not exist'
        }
        return jsonify(response), 404
    else:
        return jsonify(r_schema.dump(radio_)), 200


@app.route("/api/weather", methods=["GET"])
def weathernow():
    weather_db = WeatherNow.query.join(WeatherDay, WeatherNow.id == WeatherDay.weather_id).all()
    return jsonify(wnows_schema.dump(weather_db)), 200


@app.route("/api/weather/forecast", methods=["GET"])
def weatherforecast():
    weather_db = WeatherDay.query.all
    return jsonify(weeks_schema.dump(weather_db)), 200


@app.route("/api/weather/<string:province>", methods=["GET"])
def weatherprovince(province):

    w_province = WeatherNow.query.filter(WeatherNow.city_name.ilike('%' + province + '%')).first()
    if w_province is None:
        response = {
            'message': 'this unable to generate weather'
        }
        return jsonify(response), 404
    else:
        forecast = WeatherDay.query.filter(WeatherDay.id == w_province.id).all()
        if forecast is not None:
            print(forecast)
            return jsonify(wnow_schema.dump(w_province)), 200
