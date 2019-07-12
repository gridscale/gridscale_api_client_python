from gs_api_client.base.api import ApiBase
from gs_api_client.synchronous.method import SyncApiMethod


class SyncApi(ApiBase):

    def __init__(self, api_client, api_class, request_provider, http_info, result_as_dict):
        self._request_provider = request_provider
        super().__init__(api_client, api_class, http_info, result_as_dict)

    def _factor_api_method(self, name):
        return SyncApiMethod(
            self._api,
            name,
            self._http_info,
            self._result_as_dict,
            self._request_provider)
