import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('YD_TOKEN')


class IpDetector:
    """Класс получает географическую информацию текущего клиента по его IP
        и выгружет ее на Яндекс диск в формате JSON файла
     """
    def __init__(self):
        """Инициализирует объект

        """
        pass

    def get_myip(self):
        """Метод возвращает текущий IP адрес клиента

        Returns:
            str: IP

        """
        response = requests.get('https://api.ipify.org/',
                                params={'format': 'json'})
        if response.status_code == 200:
            ip = response.json()['ip']
            return ip
        else:
            print('Что-то пошло не так')

    def get_infoip(self):
        """Метод возвращает географическую информацию по IP адресу клиента

        Returns: dict

        """
        my_ip = self.get_myip()
        base_url = 'https://ipinfo.io'
        response = requests.get(f"{base_url}/{my_ip}/geo")

        if response.status_code == 200:
            return response.json()
        else:
            print('Что-то пошло не так')

    def get_file_infoip(self):
        """Метод возвращает географическую информацию по IP адресу клиента в формате JSON файла

        Returns:
            JSON: data_infoIP.json

        """
        infoip_dict = self.get_infoip()
        file_path = os.path.join(os.getcwd(), 'data_infoIP.json')
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(infoip_dict, f, indent=2, ensure_ascii=False)

    def create_folder(self, token: str):
        """Метод создает папку на Яндекс диске

        Args:
            token (str): Токен доступа на Яндекс диск, полученный на Полигоне
        Returns:
            str: путь к папке на Яндекс Диске с именем test

        """
        self._token = token
        base_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        folder = '/test'
        response = requests.put(base_url,
                                headers={'Authorization': f"OAuth {self._token}"},
                                params={'path': folder})
        if response.status_code in [200, 201]:
            return folder
        else:
            print('Что-то пошло не так')

    def put_file_to_yd(self, token: str):
        """Метод загружает файл JSON c географичесой информацией на Яндекс Диск

        Args:
            token (str): Токен доступа на Яндекс диск, полученный на Полигоне

        Returns:
            JSON: data_infoIP.json

        """
        self._token = token
        self._path = f"{self.create_folder(token)}/data_infoIP.json"
        self.get_file_infoip()
        base_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        response = requests.get(base_url,
                                headers={'Authorization': f"OAuth {self._token}"},
                                params={'path': self._path, 'overwrite': True})
        if response.status_code in [200, 409, 201]:
            self.get_file_infoip()
            with open('data_infoIP.json') as f:
                resp = requests.put(url=response.json()['href'], files={'file': f})
            resp.raise_for_status()
            print(resp)
        else:
            print('Что-то пошло не так')

if __name__ == "__main__":
    test = IpDetector()
    test.put_file_to_yd(TOKEN)
