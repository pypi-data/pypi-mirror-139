from authone.config import base_url
from authone.http_client import RequestsClient


class ResourceMeta(type):

    def __init__(cls, name, bases, cls_dict):
        if not hasattr(cls, '_registry'):
            cls._registry = {}
        else:
            cls._registry[name] = cls()

        super().__init__(name, bases, cls_dict)


class ResourceComponent(metaclass=ResourceMeta):

    _base_url = base_url

    def __getattr__(self, resource_name):
        if resource_name in self._registry:
            return self._registry[resource_name]
        else:
            raise AttributeError(
                '{object_name} has no attribute \'{resource_name}\''.format(
                    object_name=self.__class__.__name__,
                    resource_name=resource_name,
                ),
            )

    def setup_app_config(self, app_id, app_secret):
        self._registry['_app_id'] = app_id
        self._registry['_app_secret'] = app_secret

    def get_app_id(self):
        return self._app_id

    def get_app_secret(self):
        return self._app_secret

    def setup_request_client(self, retries, timeout, backoff_factor):
        _request_client = RequestsClient(retries, timeout, backoff_factor)

        for resource in self._registry.values():
            setattr(resource, '_request_client', _request_client)

    def _construct_url(self, url_path):
        return '{base_url}{url_path}'.format(
            base_url=self._base_url,
            url_path=url_path,
        )

    def request(self, method, url_path, params=None, data=None):
        return self._request_client.request(
            method.lower(),
            self._construct_url(url_path),
            params=params,
            data=data,
        )
