import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('YD_TOKEN')

class IpDetector()
    def __init__(self):
        pass

    def myIP(self):
        response = requests.get('https://api.ipify.org/',
                                params={'format':'json'})
        if response.status_code == 200:
            ip = response.json()['ip']
            return ip
        else:
            print('Что-то пошло не так')
