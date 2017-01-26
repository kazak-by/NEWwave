import requests
import threading
import pika
import json
from datetime import datetime

credentials = pika.PlainCredentials('kazak', 'kazak')
parameters = pika.ConnectionParameters('172.19.1.74',
                                       5672,
                                       '/',
                                       credentials)
target = open('parametrs.json', 'r')
js = json.loads(target.read())

def get_weather_json(host, minsk, ny, moscow, appid):
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    now = datetime.now()
    current_date = '%s/%s/%s %s:%s:%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    threading.Timer(300.0, get_weather_json).start()
    response = requests.get("%s/data/2.5/group?id=%s,%s,%s&units=metric&APPID=%s" % (host, minsk, ny, moscow, appid))
    print response.json()
    channel.basic_publish(exchange='',
                          routing_key='Weather',
                          body='[%s,{"current_date": "%s"}]' % (json.dumps(response.json()), current_date))
    connection.close()

get_weather_json(js['host'], js['minsk'], js['ny'], js['moscow'], js['appid'])
