from authone.resources.base import ResourceComponent


class User(ResourceComponent):

    v1_user_info_api_url = '/api/v1/sdk/userinfo/'

    def get_metadata_by_token(self, token):
        return self.request('get', self.v1_user_info_api_url, params={'token': token})
