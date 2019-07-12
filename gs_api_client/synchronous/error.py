from gs_api_client.base.error import ApiClientError


class AsynchronousApiError(ApiClientError):
    def __init__(self, request_uuid, status, message):
        self.request_uuid = request_uuid
        self.status = status
        self.message = message

    def __str__(self):
        return 'Asynchroneous request {} failed with status {} and message "{}"'.format(
            self.request_uuid,
            self.status,
            self.message)


class PollMethodArgResolveError(ApiClientError):
    def __init__(self, poll_method, arg_name):
        self.poll_method = poll_method
        self.arg_name = arg_name

    def __str__(self):
        return 'Unable to resolve argument {} for poll method {}'.format(
            self.arg_name,
            self.poll_method.__name__)
