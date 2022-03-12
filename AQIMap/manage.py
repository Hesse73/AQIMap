#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import time


def get_aqi():
    print('Aqi update daemon thread started.')
    print('waiting...')
    time.sleep(3)
    from map.aqi import waqi
    from map.models import AqiData
    fetcher = waqi()
    #Check if there is data in the database
    #or the data is too old to use
    if len(AqiData.objects.all()) == 0:
        #No weather data saved
        print('no weather data detected!')
        #load "fake" data to the database
        import json
        aqi_data = json.load(open('aqi.json','r'))
        #save to database, then fetch real data
        aqi_data_object = AqiData.init_data(aqi_data, time.time())
        aqi_data = fetcher.get_aqi()
        fetcher.dump('aqi.json')
        #save to database
        aqi_data_object = AqiData.init_data(aqi_data, time.time())
        print('new weather data saved')
    else:
        while True:
            #get the last time when data was saved
            aqi_data_object = AqiData.objects.first()
            last_time = aqi_data_object.record_time
            last_day = time.localtime(last_time).tm_yday
            now = time.time()
            now_day = time.localtime(now).tm_yday
            print('time range(min):', (now-last_time)/60)
            #if time range>24hours or the day number is different -> update it
            if now - last_time >= 60*60*24 or last_day != now_day:
                print('updating weather...')
                aqi_data = fetcher.get_aqi()
                #save to database
                aqi_data_object.update(aqi_data, time.time())
                print('new weather data saved')
            time.sleep(3600)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AQIMap.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if 'runserver' in sys.argv:
        threading.Thread(target=get_aqi, daemon=True).start()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
