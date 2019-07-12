from gs_api_client.synchronous.constants import METHOD_OBJECT_UUID_ATTR_NAME, POLL_METHOD_NAME_ATTR_NAME, \
    DO_NOT_POLL_ATTR_NAME


def set_object_uuid_attr_name(func, attr_name):
    setattr(func, METHOD_OBJECT_UUID_ATTR_NAME, attr_name)


def set_poll_method_name(func, poll_method_name):
    setattr(func, POLL_METHOD_NAME_ATTR_NAME, poll_method_name)


def do_not_poll(func):
    setattr(func, DO_NOT_POLL_ATTR_NAME, True)
