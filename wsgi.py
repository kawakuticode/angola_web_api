from application.application_factory import create_app , db

import datetime
# Globally accessible libraries
from application.utilities.weather_utilities import WeatherUtilities
from application.utilities.radio_utilities import RadioUtilities

URL_WEATHER = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
_URL = "http://radios.sapo.ao"

app = create_app()
if __name__ == "__main__":
    app.run()
