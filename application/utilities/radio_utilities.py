from datetime import datetime
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup as Bs
from requests import HTTPError
from application.models.model import Radio

_URL = "http://radios.sapo.ao"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 " \
             "Safari/537.36"
LANGUAGE = "pt-PT,pt;q=0.8,pt-BR;q=0.7"

session = requests.Session()
session.headers['User-Agent'] = USER_AGENT
session.headers['Accept-Language'] = LANGUAGE
session.headers['Content-Language'] = LANGUAGE


class RadioUtilities(object):

    @classmethod
    def get_radio_soup(cls, url):
        soup = ""
        try:
            html = session.get(url)
            soup = Bs(html.text, "html.parser")
        except HTTPError:
            print(f"get radio soup http_error with code {HTTPError}")
        except ConnectionError:
            print(f"get radio soup error_connection with code {ConnectionError}")
        finally:
            return soup

    @classmethod
    def get_radio_name(cls, radio_item):
        radio_name = ''
        names = radio_item.find_all('span')
        if len(names) != 0:
            for name in names:
                if name.string is not None:
                    radio_name = name.string
        else:
            print('error radio name not founded!')
        return radio_name

    @classmethod
    def get_radio_url(cls, radio_item):
        radio_url = ''
        url_ = radio_item.find('a')
        if url_ is not None:
            radio_url = url_.get('href')
        else:
            print('radio url not founded!')
        return radio_url

    @classmethod
    def get_radio_img(cls, radio_item):
        img_logo = ''
        src = radio_item.find('img')
        if src is not None:
            img_logo = src.get('src')
        else:
            print("src image logo not founded")
        return img_logo

    @classmethod
    def built_radio_url(cls, url, params):
        return urljoin(url, params)

    @classmethod
    def get_radio_stream_url(cls, radio_url):
        url_stream = ''
        try:
            soup = cls.get_radio_soup(radio_url)
            player = soup.find(class_="player")
            if player is not None:
                url_stream = player.find('li').find('a').get('href')
        except Exception:
            print(f"url stream error {Exception}")
        finally:
            return url_stream

    @classmethod
    def get_radio_data(cls, url):
        data_radio = {}
        try:
            soup = cls.get_radio_soup(url)
            list_radios = soup.find_all(id="radios-list")
            radio_items = [li for ul in list_radios for li in ul.findAll('li')]
            if len(list_radios) > 0 and len(radio_items) > 0:
                for radio in radio_items:
                    result = dict()
                    result['r_name'] = cls.get_radio_name(radio)
                    result['img_src'] = cls.get_radio_img(radio)
                    result['params'] = cls.get_radio_url(radio)
                    result['url_radio'] = cls.built_radio_url(url, result['params'])
                    result['stream_link'] = cls.get_radio_stream_url(result['url_radio'])
                    radio_ = (Radio(result['r_name'], result['url_radio'], result['stream_link'], result['img_src']))

                    data_radio.update({radio_.r_name: radio_})
            else:
                print(f"radio list not found")
        except HTTPError:
            print(f"get radio_webdata! Http error. code : {HTTPError}")
        except ConnectionError:
            print(f"get radio_webdata! connection error. code : {ConnectionError}")
        except Exception:
            print(f"Error while creating  radio_webdata! code: {Exception}")
        finally:
            return data_radio

    @classmethod
    def add_radio_db(cls, radio_webdata, db):
        status = False
        radio_list_db = Radio.query.all()
        try:
            if (len(radio_webdata) != 0) and (len(radio_list_db) == 0):
                db.session.add_all(list(radio_webdata.values()))
                db.session.commit()
                status = True
        except Exception:
            print(f"Error while adding radio_webdata code : {Exception}")
        finally:
            db.session.close()
            return status

    @classmethod
    def update_radio_db(cls, radio_webdata, db):
        radio_db = Radio.query.all()
        try:
            if len(radio_webdata) != 0 and len(radio_db) != 0:
                for radio_web in radio_webdata.values():
                    db.session.query(Radio). \
                        filter(Radio.r_name == radio_web.r_name). \
                        update({'r_name': radio_web.r_name, 'url': radio_web.url,
                                'stream_link': radio_web.stream_link, 'img_logo': radio_web.img_logo})
                db.session.commit()
            else:
                print(f"No need to update radios data!!")
        except Exception:
            print(f"unable to update radio_webdata {Exception}")
        finally:
            db.session.close()
