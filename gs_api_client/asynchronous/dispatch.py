from gs_api_client.base.dispatch import ApiRequestDispatcherBase


class AsyncApiRequestDispatcher(ApiRequestDispatcherBase):
    def _try_to_dispatch(self):
        self._perform_request()
