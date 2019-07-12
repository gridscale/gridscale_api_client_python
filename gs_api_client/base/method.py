from abc import ABC, abstractmethod


class ApiMethodBase(ABC):
    def __init__(self, api, method_name, http_info, result_as_dict):
        self._api = api
        self._method_name = method_name
        self._http_info = http_info
        self._result_as_dict = result_as_dict
        self._fetch_docstring_from_actual_api_method()

    def _fetch_docstring_from_actual_api_method(self):
        """
        Overwrites docstring from api method.
        Dirty hack, but allows for args/response lookups
        from interactive interpreters.
        """
        method = getattr(self._api, self._method_name)
        self.__doc__ = method.__doc__

    @abstractmethod
    def __call__(self, *a, **kw):
        pass

    def __repr__(self):
        return '{}(method_name={!r}, http_info={!r}, result_as_dict={!r})'.format(
            self.__class__.__name__,
            self._method_name,
            self._http_info,
            self._result_as_dict)
