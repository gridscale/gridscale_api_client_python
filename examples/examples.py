import sys

from pprint import pprint
from uuid import uuid4
import os
from index_by.key import index_by_key
from configloader import load_config

from gs_api_client import SyncGridscaleApiClient, GridscaleApiClient, models
from gs_api_client import Configuration


if __name__ == '__main__':

    # run `pip3 install index_by` before executing this file

    api_config = Configuration()
    # api_config.debug = True
    api_config.host = 'https://api.gridscale.io'

    #TODO: Change filename
    configfile = load_config("config.yaml")
    api_config.api_key['X-Auth-Token'] = configfile[0].get("token")
    api_config.api_key['X-Auth-UserId'] = configfile[0].get("userId")
    api_config.debug = True

    print('-' * 80)
    client = SyncGridscaleApiClient(configuration=api_config, http_info=False)

    # get locations
    get_locations_response = client.get_locations()
    locations = get_locations_response['locations'].values()
    location_by_name = index_by_key(locations, 'name')
    location = location_by_name['de/fra']

    # get templates
    get_templates_response = client.get_templates()
    templates = get_templates_response['templates'].values()
    template_by_name = index_by_key(templates, 'name')
    template = template_by_name['Debian 11']

    # create storage
    create_storage_response = client.create_storage({
        'name': 'my storage',
        'capacity': 10,
        'location_uuid': location['object_uuid'],
        'storage_type': 'storage_insane',
        'template': {
            'template_uuid': template['object_uuid'],
            'hostname': 'myserver',
            'password': 'secret_pass123!#.,'
        }
    })
    storage = create_storage_response['storage']

    # create server
    create_server_response = client.create_server({
        'name': 'my server',
        'cores': 1,
        'memory': 2,
        'location_uuid': location['object_uuid']})
    server = create_server_response['server']

    # link storage to server
    client.link_storage_to_server(
        server['object_uuid'],
        {'bootdevice': True, 'object_uuid': storage['object_uuid']})

    # start server
    client.update_server_power(
        server['object_uuid'],
        {'power': True})

    # get updated server
    get_server_response = client.get_server(server['object_uuid'])
    updated_server = get_server_response['server']
