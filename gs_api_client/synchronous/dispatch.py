import inspect
from time import sleep
from uuid import UUID

from gs_api_client.base.constants import REQUEST_UUID_RESPONSE_HEADER
from gs_api_client.base.dispatch import ApiRequestDispatcherBase

from gs_api_client.synchronous.constants import METHOD_OBJECT_UUID_ATTR_NAME, METHOD_OBJECT_UUID_ATTR_DEFAULT, \
    POLL_METHOD_NAME_ATTR_NAME, POLL_HTTP_CODE, DO_NOT_POLL_ATTR_NAME, INCORRECT_CODE_METHODS
from gs_api_client.synchronous.error import AsynchronousApiError, PollMethodArgResolveError


class PollMethodKwargsProvider:
    def __init__(self, method, poll_method, object_uuid, request_args, request_kwargs):
        self._method = method
        self._poll_method = poll_method
        self._object_uuid = object_uuid
        self._request_args = request_args
        self._request_kwargs = request_kwargs
        self._request_args_index = None
        self._arg_name = None
        self._arg_value = None
        self._object_uuid_used_as_arg_value = None
        self._poll_method_kwargs = None

    def provide(self):
        self._init()
        self._index_request_args()
        for self._arg_name in self._iter_poll_method_arg_name():
            if self._arg_in_request_args_index():
                self._fetch_arg_value_from_request_args_index()
            else:
                self._assert_object_uuid_not_yet_used_as_arg_value()
                self._fetch_object_uuid_as_arg_value()
            self._add_to_poll_method_kwargs()
        return self._poll_method_kwargs

    def _init(self):
        self._poll_method_kwargs = {}
        self._object_uuid_used_as_arg_value = False

    def _index_request_args(self):
        argspec = inspect.getfullargspec(self._method)
        index = {}
        for arg_pos, arg_name in enumerate(argspec.args[1:]):
            if arg_name in self._request_kwargs:
                arg_value = self._request_kwargs[arg_name]
            else:
                arg_value = self._request_args[arg_pos]
            index[arg_name] = arg_value
        self._request_args_index = index

    def _iter_poll_method_arg_name(self):
        argspec = inspect.getfullargspec(self._poll_method)
        for arg_name in argspec.args[1:]:
            yield arg_name

    def _arg_in_request_args_index(self):
        return self._arg_name in self._request_args_index

    def _fetch_arg_value_from_request_args_index(self):
        self._arg_value = self._request_args_index[self._arg_name]

    def _assert_object_uuid_not_yet_used_as_arg_value(self):
        if self._object_uuid_used_as_arg_value:
            raise PollMethodArgResolveError(
                self._poll_method,
                self._arg_name)

    def _fetch_object_uuid_as_arg_value(self):
        self._arg_value = self._object_uuid
        self._object_uuid_used_as_arg_value = True

    def _add_to_poll_method_kwargs(self):
        self._poll_method_kwargs[self._arg_name] = self._arg_value


class SyncApiRequestDispatcher(ApiRequestDispatcherBase):
    def __init__(self, api, method_name, request_args, request_kwargs, http_info, result_as_dict, request_provider):
        super().__init__(api, method_name, request_args, request_kwargs, http_info, result_as_dict)
        self._request_provider = request_provider
        self._options_method = None
        self._poll_method = None
        self._object_uuid_attr_name = None
        self._object_uuid = None
        self._request = None

    def _try_to_dispatch(self):
        self._fetch_options_method()
        self._fetch_poll_method()
        self._perform_request()
        if self._response_code_needs_correction():
            self._correct_response_code()
        if self._request_is_asynchronous() and self._polling_enabled_for_method():
            self._fetch_request_uuid_from_response()
            while True:
                self._fetch_request()
                if not self._request_is_pending():
                    break
                self._wait_until_next_request_update()
            self._assert_request_was_successful()
        if self._polling_enabled_for_method():
            self._fetch_object_uuid_attr_name_from_method()
            if self._object_uuid_given_in_response():
                self._fetch_object_uuid_from_response()
            else:
                self._try_to_determine_object_uuid_from_request_args()
            if self._object_uuid_found() and self._poll_method_found() and not self._method_is_delete():
                self._poll_object_as_response()

    def _fetch_options_method(self):
        self._options_method = getattr(self._api, self._method_name)

    def _fetch_poll_method(self):
        if hasattr(self._options_method, POLL_METHOD_NAME_ATTR_NAME):
            method_name = getattr(self._options_method, POLL_METHOD_NAME_ATTR_NAME)
            self._poll_method = getattr(self._api, method_name)
        else:
            self._poll_method = None

    def _response_code_needs_correction(self):
        # API v1 returns 204 for some asynchronous operations, where 202 should be returned.
        # Since this is a breaking change, it will be corrected with API v2 and fixed in the
        # client for now.
        return self._method_name in INCORRECT_CODE_METHODS

    def _correct_response_code(self):
        self._response_code = POLL_HTTP_CODE

    def _request_is_asynchronous(self):
        return self._response_code == POLL_HTTP_CODE

    def _polling_enabled_for_method(self):
        return not getattr(self._options_method, DO_NOT_POLL_ATTR_NAME, False)

    def _fetch_request_uuid_from_response(self):
        self._request_uuid = self._response_headers[REQUEST_UUID_RESPONSE_HEADER]

    def _fetch_request(self):
        self._request = self._request_provider(self._request_uuid)

    def _request_is_pending(self):
        return self._request['status'] == 'pending'

    def _wait_until_next_request_update(self):
        sleep(0.5)

    def _assert_request_was_successful(self):
        if not self._request['status'] == 'done':
            raise AsynchronousApiError(
                self._request_uuid,
                self._request['status'],
                self._request['message'])

    def _fetch_object_uuid_attr_name_from_method(self):
        self._object_uuid_attr_name = getattr(
            self._options_method,
            METHOD_OBJECT_UUID_ATTR_NAME,
            METHOD_OBJECT_UUID_ATTR_DEFAULT)

    def _object_uuid_given_in_response(self):
        if isinstance(self._response, dict):
            return self._object_uuid_attr_name in self._response
        else:
            return hasattr(self._response, self._object_uuid_attr_name)

    def _fetch_object_uuid_from_response(self):
        if isinstance(self._response, dict):
            self._object_uuid = self._response[self._object_uuid_attr_name]
        else:
            self._object_uuid = getattr(self._response, self._object_uuid_attr_name)

    def _try_to_determine_object_uuid_from_request_args(self):
        for arg in self._request_args:
            if not isinstance(arg, str):
                continue
            try:
                UUID(arg)
            except ValueError:
                continue
            else:
                self._object_uuid = arg
                break
        else:
            self._object_uuid = None

    def _object_uuid_found(self):
        return self._object_uuid is not None

    def _poll_method_found(self):
        return self._poll_method is not None

    def _method_is_delete(self):
        return self._method_name.startswith('delete_')

    def _poll_object_as_response(self):
        kwargs_provider = PollMethodKwargsProvider(
            self._method,
            self._poll_method,
            self._object_uuid,
            self._request_args,
            self._request_kwargs)
        kwargs = kwargs_provider.provide()
        self._response = self._poll_method(**kwargs)

    def _factor_result(self):
        if self._http_info:
            self._result = self._response, self._response_code, self._response_headers
        else:
            self._result = self._response