from flask import current_app as app, render_template
from flask import jsonify
from datetime import datetime
from application.models.schemas import RadioSchema, WeatherNowSchema
from application.models.model import db, Radio, WeatherNow, Forecast
from application.utilities.radio_utilities import RadioUtilities as radio_utilities
from application.utilities.weather_utilities import WeatherUtilities as weather_utilities

URL_WEATHER = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
_URL = "http://radios.sapo.ao"

r_schema = RadioSchema()
rs_schema = RadioSchema(many=True)

wnow_schema = WeatherNowSchema()
wnows_schema = WeatherNowSchema(many=True)
#function executed by scheduled job


@app.before_first_request
def before_first_request_func():
    print("server started : ", datetime.now())
    weather_data = weather_utilities.get_weather_now(URL_WEATHER)
    radios_data = radio_utilities.get_radio_data(_URL)

    if not radio_utilities.add_radio_db(radios_data, db):
        print("updating radios.... on start")
        radio_utilities.update_radio_db(radios_data, db)
    if not weather_utilities.add_weather_db(weather_data, db):
        print("updating weather now....on start")
        weather_utilities.update_weather_db(weather_data, db)




@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
@app.route("/index", methods=["GET"])
def home():
    return render_template("home.html")


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


@app.route("/api/v1/weather", methods=["GET"])
def weathernow():
    weather_db = WeatherNow.query.join(Forecast, WeatherNow.id == Forecast.weather_id).all()
    return jsonify(wnows_schema.dump(weather_db)), 200

@app.route("/api/v1/weather/<string:province>", methods=["GET"])
def weatherprovince(province):
    w_province = WeatherNow.query.filter(WeatherNow.city_name.ilike('%' + province + '%')).first()
    if w_province is None:
        response = {
            'message': 'exchange city name to capital name - unable to generate weather for --> ' + province
        }
        return jsonify(response), 404
    else:
        return jsonify(wnow_schema.dump(w_province)), 200
