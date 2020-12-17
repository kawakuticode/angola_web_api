from datetime import datetime
from datetime import timedelta

import requests
from bs4 import BeautifulSoup as Bs
from requests import HTTPError

from application.models.weather import WeatherNow, Forecast

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
    def update_progress(cls, progress):
        print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress * 50), progress * 100), end="", flush=True)

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
        progress = 0
        try:
            for region in ANGOLA_PROVINCES:

                progress += 1
                working = progress / len(ANGOLA_PROVINCES)
                cls.update_progress(working)

                temp_url = url + f"+{region}"
                soup = cls.get_weather_soup(temp_url)
                result = dict()
                # extract data
                result['city_name'] = soup.find("div", attrs={"id": "wob_loc"}).text
                result['temperature'] = soup.find("span", attrs={"id": "wob_tm"}).text
                time_tmp = soup.find("div", attrs={"id": "wob_dts"}).text
                result['time_of_day'] = cls.time_weatherdata (time_tmp)
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

                    n_day = Forecast(day_name, description, min_temp, max_temp)
                    next_days.append(n_day)

                    result['week_weather'] = next_days

                    _weather = WeatherNow(result['city_name'], result['time_of_day'], result['temperature'],
                                          result['description'], result['preciptation'], result['humidity'],
                                          result['wind'], result['week_weather'])

                data_weather.update({_weather.city_name: _weather})
        except HTTPError:
            print(f"get weather data Http error. code : {HTTPError}")
        except ConnectionError:
            print(f"get weather data now connection error. code : {ConnectionError}")
        except Exception as error:
            print(f"main error getting weather data : {error}")
        finally:
            return data_weather

    @classmethod
    def add_weather_db(cls, weather_data, db):
        weather_db = WeatherNow.query.all()
        status = False
        try:
            if (list(weather_data.values()) != 0) and (len(weather_db) == 0):
                db.session.add_all(list(weather_data.values()))
                db.session.commit()
                status = True
        except Exception:
            print(f"error adding the weather to db: {Exception}")
        finally:
            db.session.close()
            return status



    @classmethod
    def update_weather(cls,weather_database , db):
        print(weather_database)
        try:
            db.session.query(WeatherNow).filter(WeatherNow.city_name ==
                                            weather_database.city_name) \
            .update({'city_name': weather_database.city_name,
                     'time_of_day': weather_database.time_of_day,
                     'temperature': weather_database.temperature,
                     'description': weather_database.description,
                     'preciptation': weather_database.preciptation,
                     'humidity': weather_database.humidity,
                     'wind': weather_database.wind})

            for week_day in weather_database.forecast_week:
                db.session.query(Forecast).filter(Forecast.weather_id == weather_database.id,
                                              Forecast.day == week_day.day).update(
                {'day': week_day.day,
                 'description': week_day.description,
                 'min_temperature': week_day.min_temperature,
                 'max_temperature': week_day.max_temperature})

            db.session.commit()
        except Exception:
            raise Exception
            print(f"error updating the weather: {Exception}")

    @classmethod
    def update_weather_db(cls, weather_data, db):
        weather_db = WeatherNow.query.all()

        try:
            if len(weather_data.values()) != 0 and len(weather_db) != 0:
                """filter database by date to check if passed 1hr to update weather database ."""
                checked_date_weather = filter(lambda weather : cls.check_date(weather.time_of_day) , weather_db)
                """update the filtered ones"""
                updated_weather = [cls.update_weather( weather_data[weather.city_name] , db ) for weather in checked_date_weather]

                if not updated_weather :
                    print(f"No need to update Weather data !!")
        except Exception:
            raise Exception
            print(f"error updating the weather: {Exception}")
        finally:
            db.session.close()

    @classmethod
    def time_weatherdata (cls, t_stamp):

        time_system = datetime.now()
        time_weather =t_stamp.split(' ')[1] .split(':')
        w_hour = time_weather[0]
        w_minutes = time_weather[1]
        time_of_day = time_system.replace(hour=int(w_hour), minute=int(w_minutes), second=0)

        return time_of_day.strftime('%Y-%m-%d %H:%M:%S.%f')

    @classmethod
    def check_date(cls, date_db):

        condition = False
        try:
            time_db = datetime.strptime(date_db, '%Y-%m-%d %H:%M:%S.%f')
            time_now = datetime.now()
            delta_time = time_now - time_db
            diff_time_hr = delta_time.total_seconds() / 3600
            #print(diff_time_hr)

            if (diff_time_hr > 1):
                condition = True
        except  Exception:
            print("Unable to check date")
        finally:
            return condition
