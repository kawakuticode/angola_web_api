import os
from datetime import datetime
from flask_apscheduler import APScheduler
from application.utilities.weather_utilities import WeatherUtilities as weather_util
from application.utilities.radio_utilities import RadioUtilities as radio_util
import logging

from application.models.model import db

URL_WEATHER = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
_URL = "http://radios.sapo.ao"


def update_database_all(app):
    with app.app_context():
        logging.info("database update radio_db scheduled  from: %s", datetime.now())
        radios_data = radio_util.get_radio_data(_URL)
        radio_util.update_radio_db(radios_data, db)

        logging.info("database update weather_db scheduled from: %s", datetime.now())
        weather_data = weather_util.get_weather_now(URL_WEATHER)
        weather_util.update_weather_db(weather_data, db)


def register_scheduler(app):
    DEV_JOBS = [
        {'id': 'update_database',
         'func': update_database_all,
         'args': [app],
         'trigger': 'interval',
         'minutes': 3}]

    PROD_JOBS = [
        {'id': 'update_database',
         'func': update_database_all,
         'args': [app],
         'trigger': 'interval',
         'minutes': 60}]

    flask_env = app.config.get('FLASK_ENV')
    if flask_env == 'development':
        app.config.update(JOBS=DEV_JOBS)
    else:
        app.config.update(JOBS=PROD_JOBS)

    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()
