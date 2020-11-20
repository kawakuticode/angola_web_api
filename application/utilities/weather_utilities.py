from datetime import datetime

import requests
from bs4 import BeautifulSoup as Bs
from requests import HTTPError

from application.models.weather import WeatherNow, WeatherDay

URL_WEATHER = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
ANGOLA_PROVINCES = ['Bengo', 'Benguela', 'Kuito', 'Cabinda', 'Menongue', "N'dalatando", 'Sumbe', 'Ondjiva',
                    'Huambo', 'Lubango', 'Luanda', 'Dundo', 'Saurimo', 'Malanje', 'Luena', 'Namibe', 'Uíge', 'Zaire']

WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 " \
             "Safari/537.36"
LANGUAGE = "en-gb;q=0.8, en;q=0.7"

session = requests.Session()
session.headers['User-Agent'] = USER_AGENT
session.headers['Accept-Language'] = LANGUAGE
session.headers['Content-Language'] = LANGUAGE


class WeatherUtilities(object):

    @classmethod
    def get_weather_soup(cls, url):
        try:
            html = session.get(url)
            soup = Bs(html.text, "html.parser")
        except HTTPError:
            print(f"get weather soup error with code {HTTPError}")
        except ConnectionError:
            print(f"get weather soup error with code {ConnectionError}")
        finally:
            return soup

    @classmethod
    def get_weather_now(cls, url):
        data_weather = {}
        try:
            for region in ANGOLA_PROVINCES:
                temp_url = url + f"+{region}"
                soup = cls.get_weather_soup(temp_url)
                print(temp_url)
                # print(soup.prettify())
                result = dict()
                # extract data
                result['city_name'] = soup.find("div", attrs={"id": "wob_loc"}).text
                result['temperature'] = soup.find("span", attrs={"id": "wob_tm"}).text
                result['time_of_day'] = soup.find("div", attrs={"id": "wob_dts"}).text
                result['description'] = soup.find("span", attrs={"id": "wob_dc"}).text
                result['preciptation'] = soup.find("span", attrs={"id": "wob_pp"}).text
                result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
                result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text

                next_days = []
                days = soup.find("div", attrs={"id": "wob_dp"})
                for day in days.findAll("div", attrs={"class": "wob_df"}):
                    # extract the name of the day
                    day_name = day.find("div", attrs={"class": "QrNVmd Z1VzSb"}).attrs['aria-label']
                    # get weather status for that day
                    description = day.find("img").attrs["alt"]
                    temp = day.findAll("span", {"class": "wob_t"})
                    # maximum temparature in Celsius, use temp[1].text if you want fahrenheit
                    max_temp = temp[0].text
                    # minimum temparature in Celsius, use temp[3].text if you want fahrenheit
                    min_temp = temp[2].text

                    n_day = WeatherDay(day_name, description, min_temp, max_temp)
                    next_days.append(n_day)

                    result['week_weather'] = next_days

                    _weather = WeatherNow(result['city_name'], result['time_of_day'], result['temperature'],
                                          result['description'], result['preciptation'], result['humidity'],
                                          result['wind'], result['week_weather'])

                data_weather.update({_weather.city_name: _weather})
            #print (data_weather.values())
        except HTTPError:
            print(f"get weather data Http error. code : {HTTPError}")
        except ConnectionError:
            print(f"get weather data now connection error. code : {ConnectionError}")
        finally:
            return data_weather


    @classmethod
    def add_weather_now_db(cls, db):

        weather_db = WeatherNow.query.all()
        weather_dict = cls.get_weather_now(URL_WEATHER)
        weather_list = list(weather_dict.values())

        if (weather_list != 0) and (len(weather_db) == 0):
            db.session.add_all(weather_list)
            db.session.commit()

    @classmethod
    def update_weather_now_db(cls, db):

        weather_db = WeatherNow.query.all()
        weather_dict = cls.get_weather_now(URL_WEATHER)
        # weather_list = list(weather_dict.values())
        print(f"dicionario size : {len(weather_dict.values())}")

        if len(weather_dict) != 0 and len(weather_db) != 0:
            for weather in weather_db:
                if cls.check_date(weather.time_of_day):
                    temp_weather = weather_dict[weather.city_name]
                    # print(temp_weather.week_weather)
                    # print(temp_weather.week_weather.all())
                    db.session.query(WeatherNow).filter(WeatherNow.city_name ==
                                                        temp_weather.city_name).update({
                        'city_name': temp_weather.city_name,
                        'time_of_day': temp_weather.time_of_day,
                        'temperature': temp_weather.temperature,
                        'description': temp_weather.description,
                        'preciptation': temp_weather.preciptation,
                        'humidity': temp_weather.humidity,
                        'wind': temp_weather.wind})
                    for date_week in temp_weather.week_weather:
                        print(date_week)
                        db.session.query(WeatherDay).filter(WeatherDay.weather_id == weather.id).update(
                            {'day_of_week': date_week.day_of_week,
                             'description': date_week.description,
                             'min_temperature': date_week.min_temperature,
                             'max_temperature': date_week.max_temperature,
                             })
                    db.session.commit()

        else:
            print(f"No need to update Weather data !!")

    @classmethod
    def check_date(cls, date_db):

        time_now = datetime.now()
        date_to_check = date_db.split()
        day_of_week_db = date_to_check[0]
        time_hrs_minutes = date_to_check[1].split(':')
        db_hour = time_hrs_minutes[0]
        db_minute = time_hrs_minutes[1]
        index_day = WEEK.index(day_of_week_db)

        temp_date = time_now.replace(day=index_day, hour=int(db_hour), minute=int(db_minute), second=0)
        diff_hours = (time_now - temp_date).seconds / 3600
        if diff_hours >= 1:
            return True
        else:
            return False
