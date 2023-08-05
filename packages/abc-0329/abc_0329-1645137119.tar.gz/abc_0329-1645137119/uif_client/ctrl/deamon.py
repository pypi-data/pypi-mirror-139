import json
import time

import requests

SERVER_URL = 'https://uifv2ray.xyz/heart_beat'
API_KEY = '172574895'
DELAY_SECOND = 120


def HeartBeat():
    res = requests.get('http://ip-api.com/json/?lang=zh-CN').text
    res = json.loads(res)
    res['api_key'] = API_KEY
    while True:
        try:
            requests.get(SERVER_URL, params=res)
        except Exception as e:
            pass
        time.sleep(DELAY_SECOND)


HeartBeat()
