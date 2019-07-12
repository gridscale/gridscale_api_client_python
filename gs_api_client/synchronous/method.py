from gs_api_client.base.method import ApiMethodBase
from gs_api_client.synchronous.dispatch import SyncApiRequestDispatcher


class SyncApiMethod(ApiMethodBase):
    def __init__(self, api, method_name, http_info, result_as_dict, request_provider):
        super().__init__(api, method_name, http_info, result_as_dict)
        self._request_provider = request_provider

    def __call__(self, *a, **kw):
        dispatcher = SyncApiRequestDispatcher(
            self._api,
            self._method_name,
            a,
            kw,
            self._http_info,
            self._result_as_dict,
            self._request_provider)
        return dispatcher.dispatch()
