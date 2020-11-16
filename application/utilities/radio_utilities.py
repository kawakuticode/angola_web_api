from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from requests import HTTPError

from application.models.radio_station import Radio


class RadioUtilities(object):
    @classmethod
    def get_radio_name(self, radio_item):
        radio_name = ''
        names = radio_item.find_all('span')
        if len(names) != 0:
            for name in names:
                if name.string != None:
                    radio_name = name.string
        else:
            print('error radio name not founded!')
        return radio_name

    @classmethod
    def get_radio_url(self, radio_item):
        radio_url = ''
        url_ = radio_item.find('a')
        if url_ != None:
            radio_url = url_.get('href')
        else:
            print('radio url not founded!')
        return radio_url

    @classmethod
    def get_radio_img(self, radio_item):
        img_logo = ''
        src = radio_item.find('img')
        if src != None:
            img_logo = src.get('src')
        else:
            print("src image logo not founded")
        return img_logo

    @classmethod
    def built_radio_url(self, url, params):
        return urljoin(url, params)

    @classmethod
    def get_radio_stream_url(self, radio_url):
        url_stream = ''
        try:
            page = requests.get(radio_url)
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, "html.parser")
                player = soup.find(class_="player")
                link = player.find('li').find('a').get('href')
                if player != None and link != None:
                    url_stream = link
        except HTTPError:
            print(f"get stream page url error. code : {page.status_code}, {HTTPError}")
        finally:
            return url_stream

    @classmethod
    def get_radio_data_by_soup( self, url):
        radio_list = []
        try:
            page = requests.get(url)
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, "html.parser")
                list_radios = soup.find_all(id="radios-list")
                radio_items = [li for ul in list_radios for li in ul.findAll('li')]
                if len(list_radios) > 0 and len(radio_items) > 0:
                    for radio in radio_items:
                        r_name =self.get_radio_name(radio)
                        img_src = self.get_radio_img(radio)
                        params = self.get_radio_url(radio)
                        url_radio = self.built_radio_url(url, params)
                        stream_link = self.get_radio_stream_url(url_radio)
                        radio_list.append(Radio(r_name, url_radio, stream_link, img_src))
                else:
                    print(f"radio list not found")
        except HTTPError:
            print(f"get radio data error. code : {page.status_code}, {HTTPError}")
        finally:
            return radio_list

    @classmethod
    def add_or_update_radio_db (self, radio_list, db ) :
        radio_list_db = Radio.query.all()
        if (len(radio_list) != 0) and (len(radio_list_db) == 0):
            db.session.add_all(radio_list)
            db.session.commit()
        elif (radio_list != 0) and (len(radio_list_db) != 0) :
            for radio_ in radio_list :
                db.session.query(Radio).filter(Radio.r_name == radio_.r_name).update({'r_name':radio_.r_name,
                                                                                      'url':radio_.url,
                                                                                      'stream_link':radio_.stream_link,
                                                                                      'img_logo':radio_.img_logo})
                db.session.commit()
        else:
            print (f"size of radio list from scrap {radio_list}. No need to update !!")