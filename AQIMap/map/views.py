from django.shortcuts import render
from django.http import HttpResponse

import geoip2.database
import json
from map.models import AqiData
# Create your views here.


def index(request):
    def cal_color(score):
        """
        target_color = ''
        for idx in range(3):
            sub_color = (max_color[idx]-min_color[idx]) / \
                500*score+min_color[idx]
            target_color += '{:02x}'.format(int(sub_color))
        return target_color
        """
        if score < 50:
            return '#00e400'
        elif score<100:
            return '#ff0'
        elif score<150:
            return '#ff7e00'
        elif score<200:
            return '#ff0'
        elif score < 300:
            return '#99004c'
        else:
            return '#7e0023'
    #获取访问者的IP地址，然后通过geoIp转换为所在城市
    ip = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if not ip:
        ip = request.META.get('REMOTE_ADDR', "")
    client_ip = ip.split(",")[-1].strip() if ip else ""
    print('userIP:'+client_ip)
    reader = geoip2.database.Reader('./map/GeoLite2-City.mmdb')
    try:
        response = reader.city(client_ip)
        country = response.country.names["zh-CN"]
        city = response.city.names["zh-CN"]
        lng, lat = response.location.longitude, response.location.latitude
        print('country:%s, city:%s, loc:,(%f,%f)' % (country, city, lng, lat))
    except:
        print('INVALID IP')
        lng, lat = 117.2560, 31.8380
    #获取数据库中保存的天气数据
    aqi_data_object = AqiData.objects.first()
    aqi_data = aqi_data_object.aqi_data
    #转换为地图API要求的格式
    target_data = []
    for aqi in aqi_data:
        try:
            target_data.append(
                {'lng': aqi['geo'][1], 'lat': aqi['geo'][0], 'score': aqi['aqi'], 'color': cal_color(aqi['aqi'])})
        except TypeError:
            pass
        except:
            raise

    #发送天气和用户地址
    return render(request, "map/index.html", {'lng': lng,
                                              'lat': lat,
                                              'aqi_data': target_data})
