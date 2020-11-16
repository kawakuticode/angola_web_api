from urllib.parse import urljoin
from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs
from requests import HTTPError
from application.models.weather import WeatherNow, WeatherDay
import time

URL_WEATHER = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
ANGOLA_PROVINCES = ['Bengo', 'Benguela', 'Kuito', 'Cabinda', 'Menongue', "N'dalatando", 'Sumbe', 'Ondjiva',
                    'Huambo', 'Lubango', 'Luanda', 'Dundo', 'Saurimo', 'Malanje', 'Luena', 'Namibe', 'Uíge', 'Zaire']



USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
LANGUAGE = "en-gb;q=0.8, en;q=0.7"

session = requests.Session()
session.headers['User-Agent'] = USER_AGENT
session.headers['Accept-Language'] = LANGUAGE
session.headers['Content-Language'] = LANGUAGE



class WeatherUtilities(object):

    @classmethod
    def get_weather_soup(self, url):
        try:
            html = session.get(url)
            # create a new soup
            soup = bs(html.text, "html.parser")
            return soup
        except HTTPError :
            pass

    @classmethod
    def get_weather_now(self, url ):
        data_weather = []
        for region in ANGOLA_PROVINCES:
            temp_url = url + f"+{region}"
            soup = self.get_weather_soup(temp_url)
            result = {}
        # extract region
            result['city_name'] = soup.find("div", attrs={"id": "wob_loc"}).text
        # extract temperature now
            result['temperature'] = soup.find("span", attrs={"id": "wob_tm"}).text
        # get the day and hour now
            result['time_of_day'] = soup.find("div", attrs={"id": "wob_dts"}).text
        # get the actual weather
            result['description'] = soup.find("span", attrs={"id": "wob_dc"}).text
        # get the precipitation
            result['preciptation'] = soup.find("span", attrs={"id": "wob_pp"}).text
            result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
            result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text
            data_weather.append(WeatherNow(result['city_name'], result['time_of_day'], result['temperature'],
                                           result['description'], result['preciptation'],result['humidity'],result['wind']))
            temp_url = ""

        return data_weather


    @classmethod
    def get_weather_next_days(self, soup):
        result = {}
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
            next_days.append({f"day_of_week:{day_name}, description:{description}, max_temp:{max_temp}ºC, min_temp:{min_temp}ºC"})
            # append to result
            result['next_days'] = next_days

        return result

    @classmethod
    def add_update_weather_now_db (self, weather_list, db ) :
        weather_db = WeatherNow.query.all()
        if (weather_list != 0) and (len(weather_db) == 0 ):
            db.session.add_all(weather_list)
            db.session.commit()
        elif (weather_list != 0) and (len(weather_db) != 0):
                for weather in weather_list:
                    named_tuple = time.localtime()  # get struct_time
                    time_string = time.strftime("%A %H:%M", named_tuple)
                    print("="*3,">" , weather.city_name)
                    print("=" * 3, ">", weather.time_of_day)
                    print("=" * 3, ">",datetime.now().time())
                    #print("=" * 3, ">",time_string)
                    print (datetime.strptime(time_string,
                                      '%A %H:%M'))
                    print("=" * 40)
                    '''db.session.query(WeatherNow).filter(WeatherNow.city_name == weather.city_name).update({'time_of_day': weather.time_of_day,
                                                                                                            'temperature': weather.temperature,
                                                                                                            'description': weather.description,
                                                                                                            'preciptation': weather.preciptation,
                                                                                                            'humidity': weather.humidity,
                                                                                                             'wind': weather.wind})
                                        db.session.commit() '''
        else:
            print(f"size of weather list from scrap {weather_list}. No need to update !!")