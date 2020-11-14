from flask import current_app as app
from flask import jsonify


from application.models.radio_station import Radio
from application.models.radio_station import RadioSchema
from application.models.radio_station import db
from application.utilities.radio_utilities import RadioUtilities as R_uti

_URL = "http://radios.sapo.ao"

r_schema = RadioSchema()
rs_schema = RadioSchema(many=True)

@app.before_first_request
def before_first_request_func():
    radios_list = R_uti.get_radio_data_by_soup(_URL)
    if (radios_list != 0) and (len(Radio.query.all()) == 0 ):
        db.session.add_all(radios_list)
        db.session.commit()
    else:
        print("no need to update!!")


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

