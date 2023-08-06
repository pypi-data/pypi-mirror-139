from authone.resources.base import ResourceComponent


class SocialUser(ResourceComponent):

    v1_user_info_api_url = '/sdk/api/v1/social/userinfo/'

    def get_userinfo_by_token(self, token, signature):
        params = {'app_id': self.get_app_id(), 'token': token, 'signature': signature}
        return self.request('get', self.v1_user_info_api_url, params=params)
