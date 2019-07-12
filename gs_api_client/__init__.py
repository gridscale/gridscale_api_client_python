from gs_api_client.asynchronous.client import GridscaleApiClient
from gs_api_client.base.api_registry import ApiRegistry
from gs_api_client.synchronous.client import SyncGridscaleApiClient
from gs_api_client.synchronous.decorate import set_poll_method_name, set_object_uuid_attr_name
# noinspection PyUnresolvedReferences
from gs_api_client.swagger import api, models, Configuration

__all__ = ['SyncGridscaleApiClient', 'GridscaleApiClient', 'Configuration', 'models']

POLL_ACTIONS = {'create', 'update', 'delete'}


def register_apis(module, api_registry):
    for name in dir(module):
        if not name.endswith('Api'):
            continue
        api_class = getattr(module, name)
        api_registry.register(name, api_class)


def register_poll_methods(api_registry):
    for _, api_class in api_registry:
        for name in dir(api_class):
            attr = getattr(api_class, name)
            if name.startswith('_') or name.endswith('_with_http_info') or not callable(attr):
                continue
            action, resource = name.split('_', 1)
            if action not in POLL_ACTIONS:
                continue
            poll_method_name = '_'.join(['get', resource])
            set_poll_method_name(attr, poll_method_name)


api_registry = ApiRegistry()

register_apis(api, api_registry)
register_poll_methods(api_registry)
