import json

import requests

from pprint import pprint

from config import TOKEN_VK

class VKuser:
    url = "https://api.vk.com/method/"

    def __init__(self, id, token=TOKEN_VK, version='5.131'):
        self.params = {'access_token': token,
                        'id': id,
                       'v': version}

    def get_photos(self):
        get_photos_url = self.url + 'photos.get'
        get_photos_params = {'v': self.params['v'], 'owner_id': self.params['id'], 'album_id': 'profile', 'extended': 1,
                            'count': '5'}
        response = requests.get(get_photos_url, params={**self.params, **get_photos_params}).json()
        exp = response['response']['items']
        return exp

    def get_max_size(self):
        dates = self.get_photos()
        for photos in dates:
            photos['sizes'] = [max(photos['sizes'], key=lambda x: x['height'])]
        return dates

    def get_dates_for_work(self):
        info = self.get_max_size()
        file_dict = {}
        for photos in info:
            if photos['likes']['count'] in file_dict.keys():
                file_dict.update({photos['date']: (el['type'], el['url']) for el in photos['sizes']})
            else:
                file_dict.update({photos['likes']['count']: (el['type'], el['url']) for el in photos['sizes']})
        return file_dict

    def add_to_file(self):
        with open('file.json', 'w') as f:
            file_dict = self.get_dates_for_work()
            new_dict = {}
            for key, value in file_dict.items():
                new_dict.update({'filename': f'{key}.png', 'size': value[0]})
                json.dump([new_dict], f, indent=2)

class YaUser():
    def __init__(self, ya_token, id):
        self.vk_dates = VKuser(id=id)
        self.token = ya_token

    def headers(self):
        return {"Accept": "application/json", "Authorization": self.token}

    def upload(self):
        headers = self.headers()
        info = self.vk_dates.get_dates_for_work()
        new_dict = {}
        for key, value in info.items():
            new_dict.update({"filename": f"{key}.png", "url": value[1]})
            filename = new_dict["filename"]
            file_url = new_dict["url"]
            params = {"path": f"Test/{filename}", "url": file_url, "overwrite": False}
            url = "https://cloud-api.yandex.net/v1/disk/resources/upload/"
            r = requests.post(url=url, params=params, headers=headers)
            res = r.json()
        return res

if __name__ == '__main__':
    vk_id = input('Введите id: ')
    ya_token = input('Введите токен Яндекс.Диска: ')
    vk_client = VKuser(vk_id)
    ya_client = YaUser(ya_token, vk_id)
    vk_client.add_to_file()
    ya_client.upload()





        



