import json
import requests

class waqi():

    token = 'fa87be13d4dfae9765a4f22ba87e5bee2b2b5657'

    def __init__(self):
        self.city_list = json.load(open('map/city.json', 'r'))
        #self.city_list = json.load(open('map/majorcity.json', 'r'))

    def get_aqi(self):
        #use api to get weather data of different city
        self.aqi_data = []
        for city_name in self.city_list:
            data = requests.get('https://api.waqi.info/feed/%s/?token=%s' %
                                (city_name.replace("'",""), self.token))
            data = data.content.decode('utf-8')
            data = json.loads(data)
            try:
                self.aqi_data.append({
                    'city': city_name,
                    'aqi': data['data']['aqi'],
                    'geo': data['data']['city']['geo']
                })
                print('get data in city:', city_name)
            except:
                #this means there is no weather data in that city
                print('no weather data in city:', city_name)
        return self.aqi_data

    def dump(self, filename='aqi.json'):
        json.dump(self.aqi_data, open(filename, 'w'))
        
