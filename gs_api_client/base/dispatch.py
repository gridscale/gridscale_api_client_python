from abc import ABC, abstractmethod

from gs_api_client.base.constants import REQUEST_UUID_RESPONSE_HEADER
from gs_api_client.base.error import ApiError, RequestError, ApiClientError
from gs_api_client.swagger.rest import ApiException


class ApiRequestDispatcherBase(ABC):
    def __init__(self, api, method_name, request_args, request_kwargs, http_info, result_as_dict):
        self._api = api
        self._method_name = method_name
        self._request_args = request_args
        self._request_kwargs = request_kwargs
        self._http_info = http_info
        self._result_as_dict = result_as_dict
        self._method = None
        self._response = None
        self._response_code = None
        self._response_headers = None
        self._request_uuid = None
        self._result = None

    def dispatch(self):
        self._fetch_method()
        try:
            self._try_to_dispatch()
        except ApiClientError:
            raise
        except ApiException as e:
            raise ApiError(
                e.headers.get(REQUEST_UUID_RESPONSE_HEADER, '-'),
                e.status,
                e.reason,
                e.headers,
                e.body)
        except Exception as e:
            raise RequestError(e)
        else:
            self._factor_result()
            if self._result_as_dict_requested() and self._result_is_model():
                self._adapt_result_to_dict()
            return self._result

    @abstractmethod
    def _try_to_dispatch(self):
        pass

    def _fetch_method(self):
        method_name = '{}_with_http_info'.format(self._method_name)
        self._method = getattr(self._api, method_name)

    def _perform_request(self):
        self._response, self._response_code, self._response_headers = \
            self._method(*self._request_args, **self._request_kwargs)

    def _factor_result(self):
        if self._http_info:
            self._result = self._response, self._response_code, self._response_headers
        else:
            self._result = self._response

    def _result_as_dict_requested(self):
        return bool(self._result_as_dict)

    def _result_is_model(self):
        return hasattr(self._result, 'to_dict')

    def _adapt_result_to_dict(self):
        self._result = self._result.to_dict()
