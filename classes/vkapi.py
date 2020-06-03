import requests
from classes.config import Config
from flask import request


class VkApi(object):
    access_token = None

    def get_api(self, params, api_endpoint):
        if self.access_token:
            params['access_token'] = self.access_token
        params['v'] = Config.VK_API_V

        response = requests.get(Config.VK_API_URL + '/method/' + api_endpoint, params=params)
        return response.json().get('response')

    def get_oauth(self, params, api_endpoint):
        params['v'] = Config.VK_API_V

        response = requests.get(Config.VK_OAUTH_URL + '/' + api_endpoint, params=params)
        return response.json()

    def get_access_token(self, code):
        access_token = self.get_oauth({
            'client_id': Config.VK_APP_CLIENT_ID,
            'client_secret': Config.VK_APP_SECRET,
            'redirect_uri': str(request.url_root) + 'oauth',
            'code': code,
        }, 'access_token')

        if not access_token.get('access_token'):
            raise ValueError("Access token didn't returned")

        self.access_token = access_token.get('access_token')

        return self.access_token

    def get_user_info(self):
        data = self.get_api({}, 'users.get')

        if not data:
            raise ValueError("Something went wrong")

        first_user = None

        for item in data:
            first_user = item
            break

        return first_user

    def get_user_friends(self):
        data = self.get_api({'count': '5', 'fields': 'domain,photo_50'}, 'friends.get')

        if not data:
            raise ValueError("Something went wrong")

        return data
