from gs_api_client.base.client import GridscaleApiClientBase
from gs_api_client.synchronous.api import SyncApi
from gs_api_client.synchronous.request import RequestProvider


class SyncGridscaleApiClient(GridscaleApiClientBase):
    def _setup_apis(self):
        request_provider = RequestProvider(
            self,
            self.http_info)
        for _, api_class in self._api_registry:
            api = SyncApi(
                self.api_client,
                api_class,
                request_provider,
                self.http_info,
                self.result_as_dict)
            for api_method_name in dir(api):
                api_method = getattr(api, api_method_name)
                self._api_method_index[api_method_name] = api_method
