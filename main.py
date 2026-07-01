import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('YD_TOKEN')
path_YD = '/test/data_infoIP.json'

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

    def GetFileInfoIP(self):
        infoIP_dict = self.infoIP()
        with open("data_infoIP.json", "w", encoding="utf-8") as f:
            json.dump(infoIP_dict, f, indent=2,ensure_ascii=False)

    def PutFileToYD(self,token: str,path_YD: str):
        self._token = token
        self.path = path_YD
        base_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        response = requests.get(base_url,
                                headers={'Authorization':f"OAuth {self._token}"},
                                params={'path':self.path,'overwrite':True})
        if response.status_code in [200,409]:
            response2 = requests.put(url=response.json()['href'],data="data_infoIP.json")
            print(response2)
        else:
            print('Что-то пошло не так')


test = IpDetector()
test.PutFileToYD(token,path_YD)