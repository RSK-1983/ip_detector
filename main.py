import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('YD_TOKEN')

class IpDetector:
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
    def infoIP(self):
        myIP = self.myIP()
        baseURL = 'https://ipinfo.io'
        response = requests.get(f"{baseURL}/{myIP}/geo")

        if response.status_code == 200:
            return response.json()
        else:
            print('Что-то пошло не так')
