from flask import current_app as app
from flask import jsonify


from application.models.radio_station import Radio
from application.models.weather import WeatherNow , WeatherDay , WeatherDaySchema, WeatherNowSchema
from application.models.radio_station import RadioSchema
from application.models.radio_station import db
from application.utilities.radio_utilities import RadioUtilities as R_uti
from application.utilities.weather_utilities import WeatherUtilities as W_uti

_URL = "http://radios.sapo.ao"
URL_WEATHER = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
ANGOLA_PROVINCES = ['Bengo', 'Benguela', 'Kuito', 'Cabinda', 'Menongue', "N'dalatando", 'Sumbe', 'Ondjiva',
                    'Huambo', 'Lubango', 'Luanda', 'Dundo', 'Saurimo', 'Malanje', 'Luena', 'Namibe', 'Uíge', 'Zaire']

r_schema = RadioSchema()
rs_schema = RadioSchema(many=True)

wnow_schema = WeatherNowSchema()
wnows_schema = WeatherNowSchema(many=True)
wday_schema = WeatherDaySchema()
wdays_schema = WeatherDaySchema(many=True)



@app.before_first_request
def before_first_request_func():
    print("print called before first request")
    radio_list = R_uti.get_radio_data_by_soup(_URL)
    weather_now_list = W_uti.get_weather_now(URL_WEATHER)
    R_uti.add_or_update_radio_db (radio_list , db)
    W_uti.add_update_weather_now_db(weather_now_list, db)


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


@app.route("/api/v1/<string:radio_name>", methods=["GET"])
def get_radio_name(radio_name):
    radio_ = Radio.query.filter_by(r_name=radio_name).first()
    if radio_ is None:
        response = {
            'message': 'this radio does not exist'
        }
        return jsonify(response), 404
    else :
        return jsonify(r_schema.dump(radio_)), 200

@app.route("/api/v1/weathernow", methods=["GET"])
def weathernow():
    weather_db = WeatherNow.query.all()
    return jsonify(wnows_schema.dump(weather_db)), 200

@app.route("/api/v1/weathernext", methods=["GET"])
def weathernext():
    for region in ANGOLA_PROVINCES:
        temp_url = URL_WEATHER+f"+{region}"
        soup = W_uti.get_weather_soup(temp_url)
        weather = W_uti.get_weather_next_days(soup)
        temp_url = ""
        print(weather)
        return jsonify(), 200

