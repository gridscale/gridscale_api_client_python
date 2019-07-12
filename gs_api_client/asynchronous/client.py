from gs_api_client.asynchronous.api import AsyncApi
from gs_api_client.base.client import GridscaleApiClientBase


class GridscaleApiClient(GridscaleApiClientBase):
    def _setup_apis(self):
        for name, api_class in self._api_registry:
            api = AsyncApi(
                self.api_client,
                api_class,
                self.http_info,
                self.result_as_dict)
            for api_method_name in dir(api):
                api_method = getattr(api, api_method_name)
                self._api_method_index[api_method_name] = api_method
