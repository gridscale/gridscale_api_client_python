class RequestProvider:
    def __init__(self, api, http_info):
        self._api = api
        self._http_info = http_info

    def __call__(self, request_uuid):
        response = self._api.get_request(request_uuid)
        requests = response[0] if self._http_info else response
        request = requests[request_uuid]
        return request
