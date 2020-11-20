from flask import current_app as app
from flask import jsonify

from application.models.radio_station import Radio
from application.models.radio_station import RadioSchema
from application.models.weather import WeatherDay, WeatherDaySchema
from application.models.weather import WeatherNow, WeatherNowSchema

URL_WEATHER = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
ANGOLA_PROVINCES = ['Bengo', 'Benguela', 'Kuito', 'Cabinda', 'Menongue', "N'dalatando", 'Sumbe', 'Ondjiva',
                    'Huambo', 'Lubango', 'Luanda', 'Dundo', 'Saurimo', 'Malanje', 'Luena', 'Namibe', 'Uíge', 'Zaire']

r_schema = RadioSchema()
rs_schema = RadioSchema(many=True)

wnow_schema = WeatherNowSchema()
wnows_schema = WeatherNowSchema(many=True)
week_schema = WeatherDaySchema()
weeks_schema = WeatherDaySchema(many=True)


@app.before_first_request
def before_first_request_func():
    # W_uti.add_weather_now_db(db)
    # print("print called before first request")
    # if not R_uti.add_radio_db(db) :
    #    print("updating radios....")
    #   R_uti.update_radio_db(db)
    # W_uti.add_weather_now_db(db)
    print("updating weather now....")
    # W_uti.update_weather_now_db(db)


@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
@app.route("/index", methods=["GET"])
def home():
    return "welcome to angola web api!"


@app.route("/api/v1/radios", methods=["GET"])
def radios():
    radios_db = Radio.query.all()
    return jsonify(rs_schema.dump(radios_db)), 200


@app.route("/api/v1/<int:radio_id>", methods=["GET"])
def get_radio_by_id(radio_id):
    radio_ = Radio.query.filter_by(id=radio_id).first()
    if radio_ is None:
        response = {
            'message': 'this radio does not exist'
        }
        return jsonify(response), 404
    else :
        return jsonify(r_schema.dump(radio_)), 200


@app.route("/api/v1/radio/<string:radio_name>", methods=["GET"])
def get_radio_name(radio_name):
    radio_ = Radio.query.filter_by(r_name=radio_name).first()
    if radio_ is None:
        response = {
            'message': 'this radio does not exist'
        }
        return jsonify(response), 404
    else:
        return jsonify(r_schema.dump(radio_)), 200


@app.route("/api/v1/weathernow", methods=["GET"])
def weathernow():
    weather_db = WeatherNow.query.all()
    return jsonify(wnows_schema.dump(weather_db)), 200


@app.route("/api/v1/weathernext", methods=["GET"])
def weathernext():
    weather_db = WeatherDay.query.all()
    return jsonify(weeks_schema.dump(weather_db)), 200


@app.route("/api/v1/weather/<string:province>", methods=["GET"])
def weatherprovince(province):
    w_province = WeatherNow.query.filter(WeatherNow.city_name.ilike('%' + province + '%')).first()
    if w_province is None:
        response = {
            'message': 'this unable to generate weather'
        }
        return jsonify(response), 404
    else:
        return jsonify(wnow_schema.dump(w_province)), 200
