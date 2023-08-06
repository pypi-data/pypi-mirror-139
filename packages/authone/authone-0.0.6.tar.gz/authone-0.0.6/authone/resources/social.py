from authone.resources.base import ResourceComponent
from authone.utils.chaos import generate_sha256_string, generate_os_urandom_string
from authone.utils.time import epoch_time_now


class SocialUser(ResourceComponent):

    v1_user_info_api_url = '/sdk/api/v1/social/userinfo/'

    def get_userinfo_by_token(self, token):
        nonce = generate_os_urandom_string(64)
        ts = epoch_time_now()

        app_id = self.get_app_id()
        app_secret = self.get_app_secret()

        input_string = "{}{}{}{}".format(
            app_id,
            app_secret,
            nonce,
            str(ts)
        )
        signature = generate_sha256_string(input_string)

        params = {'app_id': app_id, 'token': token, 'signature': signature, 'ts': str(ts), 'nonce': nonce}
        return self.request('get', self.v1_user_info_api_url, params=params)
