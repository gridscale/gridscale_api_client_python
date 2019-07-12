class ApiClientError(Exception):
    pass


class RequestError(ApiClientError):
    def __init__(self, e):
        self.e = e

    def __str__(self):
        return 'Request failed with: {!r}'.format(self.e)


class ApiError(ApiClientError):
    def __init__(self, request_uuid, code, reason, headers, body):
        self.request_uuid = request_uuid
        self.code = code
        self.reason = reason
        self.headers = headers
        self.body = body

    def __str__(self):
        return 'Request {} failed with code {}, reason "{}" and body: {}'.format(
            self.request_uuid,
            self.code,
            self.reason,
            self.body if len(self.body) < 256 else '{}...'.format(self.body[:256]))
