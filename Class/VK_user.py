import requests
from pprint import pprint


TOKEN_VK = 'THIS IS YOUR TOKEN'


class UsersVK:

    def __init__(self):
        self.vk_token = TOKEN_VK
        self.url = 'https://api.vk.com/method/'
        self.params = {
            'access_token': self.vk_token,
            'v': '5.131'
        }

    def get_groups_id(self, user_id):
        params = {
            'extended': 1,
            'user_id': user_id,
            'count': 1000
        }
        url = self.url + 'groups.get'
        res = requests.get(url, params={**self.params, **params}).json()
        return res['response']['items']

    def get_group_wall(self, user_id, name_group: str, count=10):
        url = self.url + 'wall.get'
        list_groups = self.get_groups_id(user_id)
        for group in list_groups:
            if group['name'] == name_group:
                params = {
                    'owner_id': '-' + str(group['id']),
                    'count': count,
                    'filter': 'all',
                }
                res = requests.get(url, params={**self.params, **params}).json()
                return res['response']['items']

    def get_content(self, user_id, name_group: str, count=10):
        list_info_post = self.get_group_wall(user_id, name_group, count)
        data = {}
        for info in list_info_post:
            if info['attachments'][0]['type'] == 'photo':
                type_sizes = ['w', 'z', 'y', 'x', 'm', 's']
                url_photo = []
                for post in info['attachments']:
                    for alpha in type_sizes:
                        size = [x for x in post['photo']['sizes'] if x['type'] == alpha]
                        if size:
                            break
                    url_photo.append(size[0]['url'])
                data.setdefault(info['id'], {
                    'text': info['text'],
                    'url': url_photo
                })

        return data


if __name__ == "__main__":
    user = UsersVK()
    pprint(user.get_content(35819334, '/dev/null'))
