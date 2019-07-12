from abc import ABC, abstractmethod


class ApiBase(ABC):
    def __init__(self, api_client, api_class, http_info, result_as_dict):
        self._api_client = api_client
        self._api_class = api_class
        self._http_info = http_info
        self._result_as_dict = result_as_dict
        self._api = api_class(api_client)
        self.__attributes = None
        self._init_attributes()

    def _init_attributes(self):
        own_attributes = list(self.__dict__.keys())
        public_api_attributes = [
            name
            for name in dir(self._api)
            if not name.startswith('_') and not name.endswith('_with_http_info') and callable(getattr(self._api, name))]
        self.__attributes = set(own_attributes + public_api_attributes)

    def __repr__(self):
        return '{}(api_class={!r}, http_info={!r}, result_as_dict={!r})'.format(
            self.__class__.__name__,
            self._api_class,
            self._http_info,
            self._result_as_dict)

    def __dir__(self):
        return list(self.__attributes)

    def __getattr__(self, name):
        if name in self.__attributes:
            return self._factor_api_method(name)
        raise AttributeError(name)

    @abstractmethod
    def _factor_api_method(self, name):
        pass
