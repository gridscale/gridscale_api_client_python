from abc import ABC, abstractmethod

from gs_api_client.base.api_registry import ApiRegistry
from gs_api_client.swagger import ApiClient
from gs_api_client.base.error import MultipleAuthKeyError


class MutableBoolean:
    def __init__(self, value):
        self._value = bool(value)

    def set_true(self):
        self._value = True

    def set_false(self):
        self._value = False

    def __bool__(self):
        return self._value

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self._value)


class GridscaleApiClientBase(ABC):
    def __init__(self, api_client=None, api_registry=ApiRegistry(), http_info=False, result_as_dict=True, **kw):
        self.api_client = api_client if api_client else ApiClient(**kw)
        self._api_registry = api_registry
        self.http_info = MutableBoolean(http_info)
        self.result_as_dict = MutableBoolean(result_as_dict)
        self._api_method_index = {}
        self._setup_apis()
        self.check_multiple_auth_key()

    def __dir__(self):
        return list(self.__dict__.keys()) + list(self._api_method_index.keys())

    @abstractmethod
    def _setup_apis(self):
        pass

    def check_multiple_auth_key(self):

        api_key = self.api_client.configuration.api_key

        if 'X-Auth-ServiceToken' in api_key and ('X-Auth-Token' in api_key or 'X-Auth-UserId' in api_key):
            raise MultipleAuthKeyError(code=400, reason='Ambigous authentication method, please provide only one '
                                                        'method of authentication')

    def __getattr__(self, name):
        try:
            return self._api_method_index[name]
        except KeyError:
            raise AttributeError(name)

    def __repr__(self):
        return '{}(host={!r}, http_info={!r}, result_as_dict={!r})'.format(
            self.__class__.__name__,
            self.api_client.configuration.host,
            self.http_info,
            self.result_as_dict)
