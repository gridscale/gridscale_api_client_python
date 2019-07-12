This the official Python wrapper for gridscale's [API](https://gridscale.io/en//api-documentation/index.html). Allowing you to manage your own infrastructure from your own applications.

# Prerequisites

First, the Python programming language needs to be installed. This can be done by using the [official downloads](https://www.python.org/downloads/) page.

Once done, download and install via [pypi](https://pypi.org)

`pip3 install gs_api_client`

# Introduction
First, you will need your [API credentials](https://my.gridscale.io/Easy/APIs/).

In the [examples.py](examples/examples.py) replace the `AUTH_TOKEN` & `USER_UUID` with your credentials.

# Authentication

These imports and configs need to be setup before other commands can be run. If you do not need synchronous or asynchronous requests, you can leave out `SyncGridscaleApiClient` & `GridscaleApiClient` respectively.

```python
from gs_api_client import Configuration
from gs_api_client import SyncGridscaleApiClient, GridscaleApiClient

# Initiate the configuration
api_config = Configuration()
api_config.api_key['X-Auth-Token'] = "AUTH_TOKEN"
api_config.api_key['X-Auth-UserId'] = "USER_UUID"

# Setup the client
sync_api = SyncGridscaleApiClient(configuration=api_config)
async_api = GridscaleApiClient(configuration=api_config)
```

# Async vs Sync Clients

We provide two clients `SyncGridscaleApiClient` & `GridscaleApiClient`. gridscale's API performs long running operations asynchronously in the background while returning a 202 response code, with the request identifier in the `x-request-id` response header.

The main differences are:
- `GridscaleApiClient` exposes bare gridscale API functionality, while `SyncGridscaleApiClient` adds a convenience layer on top.
- `SyncGridscaleApiClient` determines whether the request is sync or async.
- Makes asynchronous operations behave as if they were synchronous:
  - The client will block until the request has finished, successful or not.
  - Throws an `AsynchronousApiError` exception, in the case of failure.
- With most `PATCH` and `POST` requests, the synchronous client will return the resulting object instead of an empty body or just the reference.

# Debugging

Adding this line below, will output further information for debugging

```Python
api_config.debug = True
```

# Access response header

Adding `http_info=True` when instantiating the client, return value will be a tuple of response, response code and response headers (dict).

```Python
sync_api = SyncGridscaleApiClient(http_info=True)
async_api = GridscaleApiClient(http_info=True)
```

# Basic request examples
    from pprint import pprint

    # Get all Servers
    pprint(async_api.get_servers())

    # Create a Server
    pprint(async_api.create_server({'name':'test', 'cores': 1, 'memory': 2}))

    # Update a Server
    pprint(async_api.update_server('<UUID>', {
        'name':'windows production Server',
        'cores': 2,
        'memory': 4
        }))

    # Delete a Server
    pprint(client.delete_storage('<UUID>'))

# Exhaustive list of all functions

Inside the [examples.py](examples/examples.py) file, you can see some example requests to get your started. All endpoints are fully documented in our [API](https://gridscale.io/en//api-documentation/index.html)

## Requests

- get_request

## Locations

- get_locations
- get_location
- get_location_ips
- get_location_isoimages
- get_location_networks
- get_location_servers
- get_location_snapshots
- get_location_storages
- get_location_templates

## Servers

- get_servers
- get_server
- create_server
- update_server
- delete_server
- get_deleted_servers
- get_server_events
- get_server_metrics
- get_server_power
- update_server_power
- server_power_shutdown

### Server Relations

- get_server_linked_ip
- get_server_linked_ips
- get_server_linked_isoimage
- get_server_linked_isoimages
- get_server_linked_network
- get_server_linked_networks
- get_server_linked_storage
- get_server_linked_storages
- link_ip_to_server',
- link_isoimage_to_server
- link_network_to_server
- link_storage_to_server
- update_server_linked_isoimage
- update_server_linked_network
- update_server_linked_storage
- unlink_ip_from_server
- unlink_isoimage_from_server
- unlink_network_from_server
- unlink_storage_from_server

## Storages

- get_storages
- get_storage
- create_storage
- delete_storage
- get_deleted_storages
- storage_rollback
- update_storage
- get_storage_events

### Snapshots

- get_snapshots
- get_snapshot
- create_snapshot
- delete_snapshot
- get_snapshot_schedule
- get_snapshot_schedules
- update_snapshot
- create_snapshot_schedule
- update_snapshot_schedule
- delete_snapshot_schedule
- snapshot_export_to_s3
- get_deleted_snapshots

### Templates

- get_templates
- get_template
- create_template
- update_template
- delete_template
- get_template_events
- get_deleted_templates

### Marketplace Templates

- get_marketplace_templates
- get_marketplace_template
- create_marketplace_template
- update_marketplace_template
- delete_marketplace_template
- get_marketplace_template_events

## Networks

- get_network
- get_networks
- create_network
- update_network
- delete_network
- get_network_events
- get_deleted_networks

## IPs

- get_ips
- get_ip
- create_ip
- update_ip
- delete_ip
- get_ip_events
- get_deleted_ips

## Load Balancers

- get_loadbalancers
- get_loadbalancer
- create_loadbalancer
- update_loadbalancer
- delete_loadbalancer
- get_loadbalancer_events

## PaaS

- get_paas_services
- get_paas_service
- create_paas_service
- update_paas_service
- delete_paas_service
- get_paas_service_metrics
- get_paas_security_zones
- get_paas_security_zone
- create_paas_security_zone
- update_paas_security_zone
- delete_paas_security_zone
- get_paas_service_templates
- get_deleted_paas_services

## Firewalls

- get_firewalls
- get_firewall
- create_firewall
- update_firewall
- delete_firewall
- get_firewall_events

## Iso Images

- get_isoimages
- get_isoimage
- create_isoimage
- update_isoimage
- delete_isoimage
- get_isoimage_events
- get_deleted_isoimages

## Labels

- get_labels
- create_label
- delete_label

## SSH Keys

- get_ssh_keys
- get_ssh_key
- create_ssh_key
- update_ssh_key
- delete_ssh_key
- get_ssh_key_events

## Events

- event_get_all

## Object Storage

- get_buckets
- get_access_keys
- get_access_key
- create_access_key
- delete_access_key
