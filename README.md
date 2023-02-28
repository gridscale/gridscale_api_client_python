# gridscale_api_client_python

This the official Python wrapper for gridscale's [API](https://gridscale.io/en//api-documentation/index.html). Allowing you to manage your own infrastructure from your own applications.

## Prerequisites

First, the Python programming language needs to be installed. This can be done by using the [official downloads](https://www.python.org/downloads/) page.

Once done, download and install via [PyPI](https://pypi.org)

```shell
$ pip3 install gs_api_client
```

## Introduction

First, you will need your [API credentials](https://my.gridscale.io/Easy/APIs/).

In the [examples.py](https://github.com/gridscale/gridscale_api_client_python/blob/develop/examples/examples.py) replace the `AUTH_TOKEN` & `USER_UUID` with your credentials.

## Authentication

These imports and configs need to be setup before other commands can be run. If you do not need synchronous or asynchronous requests, you can leave out `SyncGridscaleApiClient` & `GridscaleApiClient` respectively.

```python
from gs_api_client import Configuration
from gs_api_client import SyncGridscaleApiClient, GridscaleApiClient

# Initiate the configuration
config = Configuration()
config.api_key['X-Auth-Token'] = "AUTH_TOKEN"
config.api_key['X-Auth-UserId'] = "USER_UUID"

# Setup the client
sync_api = SyncGridscaleApiClient(configuration=config)
async_api = GridscaleApiClient(configuration=config)
```

## Async vs. sync client

We provide two clients `SyncGridscaleApiClient` and `GridscaleApiClient`. gridscale's API performs long running operations asynchronously in the background while returning a 202 response code, with the request identifier in the `x-request-id` response header.

The main differences are:

- `GridscaleApiClient` exposes bare gridscale API functionality, while `SyncGridscaleApiClient` adds a convenience layer on top.
- `SyncGridscaleApiClient` determines whether the request is sync or async.
- Makes asynchronous operations behave as if they were synchronous:
  - The client will block until the request has finished, successful or not.
  - Throws an `AsynchronousApiError` exception, in the case of failure.
- With most `PATCH` and `POST` requests, the synchronous client will return the resulting object instead of an empty body or just the reference.

## Debugging

Adding this line below, will output further information for debugging

```python
config.debug = True
```

## Access response header

Adding `http_info=True` when instantiating the client, return value will be a tuple of response, response code and response headers (dict).

```python
sync_api = SyncGridscaleApiClient(http_info=True)
async_api = GridscaleApiClient(http_info=True)
```

## Basic request examples

```python
from pprint import pprint

# Get all servers
pprint(async_api.get_servers())

# Create a server
pprint(async_api.create_server({'name':'test', 'cores': 1, 'memory': 2}))

# Update a server
pprint(async_api.update_server('<UUID>', {
    'name':'windows production Server',
    'cores': 2,
    'memory': 4
    }))

# Delete a server
pprint(client.delete_storage('<UUID>'))
```

## Exhaustive list of all functions

Inside the [examples.py](examples/examples.py) file, you can see some example requests to get your started. All endpoints are fully documented in our [API](https://gridscale.io/en//api-documentation/index.html)

### Requests

- get_request

### Locations

- get_locations
- get_location

### Servers

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

### Server relations

- get_server_linked_ip
- get_server_linked_ips
- get_server_linked_isoimage
- get_server_linked_isoimages
- get_server_linked_network
- get_server_linked_networks
- get_server_linked_storage
- get_server_linked_storages
- link_ip_to_server
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

### Storages

- get_storages
- get_storage
- create_storage
- delete_storage
- get_deleted_storages
- storage_clone
- storage_rollback
- update_storage
- get_storage_events

### Backups

- get_storage_backups
- delete_storage_backup
- rollback_storage_backup

### Storage Backup Schedule

- get_storage_backup_chedules
- create_storage_backup_schedule
- get_storage_backup_schedule
- delete_storage_backup_schedule
- update_storage_backup_schedule

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

### Marketplace applications

- get_marketplace_applications
- get_marketplace_application
- create_marketplace_application
- update_marketplace_application
- delete_marketplace_application
- get_marketplace_application_events

### Networks

- get_network
- get_networks
- create_network
- update_network
- delete_network
- get_network_events
- get_deleted_networks
- get_network_pinned_servers()
- update_network_pinned_server()
- delete_network_pinned_server()

### IP addresses

- get_ips
- get_ip
- create_ip
- update_ip
- delete_ip
- get_ip_events
- get_deleted_ips

### Load balancers

- get_loadbalancers
- get_loadbalancer
- create_loadbalancer
- update_loadbalancer
- delete_loadbalancer
- get_loadbalancer_events
- get_deleted_loadbalancers

### PaaS

- get_paas_services
- get_paas_service
- create_paas_service
- update_paas_service
- delete_paas_service
- renew_paas_service_credentials
- get_paas_service_metrics
- get_paas_security_zones
- get_paas_security_zone
- create_paas_security_zone
- update_paas_security_zone
- delete_paas_security_zone
- get_paas_service_templates
- get_deleted_paas_services

### Firewalls

- get_firewalls
- get_firewall
- create_firewall
- update_firewall
- delete_firewall
- get_firewall_events

### ISO images

- get_isoimages
- get_isoimage
- create_isoimage
- update_isoimage
- delete_isoimage
- get_isoimage_events
- get_deleted_isoimages

### Labels

- get_labels
- get_label

### SSH keys

- get_ssh_keys
- get_ssh_key
- create_ssh_key
- update_ssh_key
- delete_ssh_key
- get_ssh_key_events

### Events

- event_get_all

### Object storage

- get_buckets
- get_access_keys
- get_access_key
- create_access_key
- delete_access_key

### Certificates

- get_certificates()
- create_certificate()
- get_certificate()
- delete_certificate()

### Usages

- project_level_usage_get()
- project_level_server_usage_get()
- project_level_distributed_storage_usage_get()
- project_level_rocket_storage_usage_get()
- project_level_storage_backup_usage_get()
- project_level_snapshot_usage_get()
- project_level_template_usage_get()
- project_level_isoimage_usage_get()
- project_level_ip_usage_get()
- project_level_loadbalancer_usage_get()
- project_level_paas_service_usage_get()
- contract_level_usage_get()
- contract_level_server_usage_get()
- contract_level_distributed_storage_usage_get()
- contract_level_rocket_storage_usage_get()
- contract_level_storage_backup_usage_get()
- contract_level_snapshot_usage_get()
- contract_level_template_usage_get()
- contract_level_isoimage_usage_get()
- contract_level_ip_usage_get()
- contract_level_loadbalancer_usage_get()
- contract_level_paas_service_usage_get()

## Development

Create a virtual environment with all necessary dependencies and run the tests as follows:

```shell
$ python -m venv .venv
$ source .venv/bin/activate
$ python -m pip install -r dev-requirements.txt
$ pytest
```

Have fun!
