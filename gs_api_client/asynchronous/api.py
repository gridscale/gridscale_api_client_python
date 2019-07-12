from gs_api_client.asynchronous.method import AsyncApiMethod
from gs_api_client.base.api import ApiBase


class AsyncApi(ApiBase):
    def _factor_api_method(self, name):
        return AsyncApiMethod(
                self._api,
                name,
                self._http_info,
                self._result_as_dict)
