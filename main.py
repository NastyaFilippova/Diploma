import json

import requests

from pprint import pprint

token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'

class VKuser:
    url = "https://api.vk.com/method/"
    version = '5.131'

    def __init__(self, token, id):
        self.params = {'access_token': token,
                        'id': id}

    def get_photos(self):
        get_photos_url = self.url + 'photos.get'
        get_photos_params = {'v': self.version, 'owner_id': self.params['id'], 'album_id': 'profile', 'extended': 1,
                            'count': '5'}
        response = requests.get(get_photos_url, params={**self.params, **get_photos_params}).json()
        exp = response['response']['items']
        for photos in exp:
            photos['sizes'] = [max(photos['sizes'], key=lambda x: x['height'])]
        return exp

    def add_to_file(self):
        with open('file.json', 'w') as f:
            info = self.get_photos()
            file_dict = {}
            for photos in info:
                if photos['likes']['count'] in file_dict.keys():
                    file_dict.update({photos['date']: str(el['type']) for el in photos['sizes']})
                else:
                    file_dict.update({photos['likes']['count']: str(el['type']) for el in photos['sizes']})
            new_dict = {}
            for key, value in file_dict.items():
                new_dict.update({'filename': f'{key}.png', 'size': value})
                date_in_file = json.dump([new_dict], f, indent=2)

    def headers(self):
        return {"Accept": "application/json", "Authorization": "TOKEN"}

    def upload(self):
        headers = self.headers()
        info = self.get_photos()
        file_dict = {}
        for photos in info:
            if photos["likes"]["count"] in file_dict.keys():
                file_dict.update({photos["date"]: str(el["url"]) for el in photos["sizes"]})
            else:
                file_dict.update({photos["likes"]["count"]: str(el["url"]) for el in photos["sizes"]})
        new_dict = {}
        for key, value in file_dict.items():
            new_dict.update({"filename": f"{key}.png", "url": value})
            filename = new_dict["filename"]
            file_url = new_dict["url"]
            params = {"path": f"Test/{filename}", "url": file_url, "overwrite": False}
            url = "https://cloud-api.yandex.net/v1/disk/resources/upload/"
            r = requests.post(url=url, params=params, headers=headers)
            res = r.json()
        return res

vk_client = VKuser(token, '552934290')
pprint(vk_client.upload())





        



