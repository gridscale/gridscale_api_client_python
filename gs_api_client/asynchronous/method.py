from gs_api_client.asynchronous.dispatch import AsyncApiRequestDispatcher
from gs_api_client.base.method import ApiMethodBase


class AsyncApiMethod(ApiMethodBase):
    def __call__(self, *a, **kw):
        dispatcher = AsyncApiRequestDispatcher(
            self._api,
            self._method_name,
            a,
            kw,
            self._http_info,
            self._result_as_dict)
        return dispatcher.dispatch()
