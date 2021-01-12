# coding: utf-8

"""
    API Specification

    # Introduction Welcome to gridscales API documentation.  A REST API is a programming interface that allows you to access and send data directly to our systems using HTTPS requests, without the need to use a web GUI. All the functionality you are already familiar with in your control panel is accessible through the API, including expert methods that are only available through the API. Allowing you to script any actions you require, regardless of their complexity.  First we will start with a general overview about how the API works, followed by an extensive list of each endpoint, describing them in great detail.  ## Requests  For security, gridscale requires all API requests are made through the HTTPS protocol so that traffic is encrypted. The following table displays the different type of requests that the interface responds to, depending on the action you require.  | Method | Description | | --- | --- | | GET | A simple search of information. The response is a JSON object. Requests using GET are always read-only. | | POST | Adds new objects and object relations. The POST request must contain all the required parameters in the form of a JSON object. | | PATCH | Changes an object or an object relation. The parameters in PATCH requests are usually optional, so only the changed parameters must be specified in a JSON object. | | DELETE | Deletes an object or object relation. The object is deleted if it exists. | | OPTIONS | Get an extensive list of the servers support methods and characteristics. We will not give example OPTION requests on each endpoint, as they are extensive and self-descriptive. |  <aside class=\"notice\"> The methods PATCH and DELETE are idempotent - that is, a request with identical parameters can be sent several times, and it doesn't change the result. </aside>  ## Status Codes  | HTTP Status | `Message` | Description | | --- | --- | --- | | 200 | `OK` | The request has been successfully processed and the result of the request is transmitted in the response. | | 202 | `Accepted` | The request has been accepted, but will run at a later date. Meaning we can not guarantee the success of the request. You should poll the request to be notified once the resource has been provisioned - see the requests endpoint on how to poll. | | 204 | `No Content` | The request was successful, but the answer deliberately contains no data. | | 400 | `Bad Request` | The request message was built incorrectly. | | 401 | `Unauthorised` | The request can not be performed without a valid authentication. X-Auth UserId or X-Auth token HTTP header is not set or the userID / token is invalid. | | 402 | `Payment Required` | Action can not be executed - not provided any or invalid payment methods. | | 403 | `Forbidden` | The request was not carried out due to lack of authorization of the user or because an impossible action was requested. | | 404 | `Not Found` | The requested resource was not found. Will also be used if you do a resource exists, but the user does not have permission for it. | | 405 | `Method Not Allowed` | The request may be made only with other HTTP methods (eg GET rather than POST). | | 409 | `Conflict` | The request was made under false assumptions. For example, a user can not be created twice with the same email. | | 415 | `Unsupported Media Type` | The contents of the request have been submitted with an invalid media type. All POST or PATCH requests must have \"Content-Type : application / json\" as a header, and send a JSON object as a payload. | | 416 | `Requested Range Not Satisfiable` | The request could not be fulfilled. It is possible that a resource limit was reached or an IPv4 address pool is exhausted. | | 424 | `Failed Dependency` | The request could not be performed because the object is in the wrong status. | | 429 | `Too Many Requests` | The request has been rejected because rate limits have been exceeded. |  <aside class=\"success\"> Status 200-204 indicates that the request has been accepted and is processed. </aside> <aside class=\"notice\"> Status 400-429 indicates that there was a problem with the request that originated on the client. You will find more information about the problem in the body of 4xx response. </aside> <aside class=\"warning\"> A status 500 means that there was a server-side problem and your request can not be processed now. </aside>  ## Request Headers  | Header | Description | | --- | --- | | Content-Type | Always \"application/json\". | | X-Auth-userId | The user UUID. This can be found in the panel under \"API\" and will never change ( even after the change of user e-mail). | | X-Auth-Token | Is generated from the API hash and must be sent with all API requests. Both the token and its permissions can be configured in the panel.|  ## Response Headers  | Header | Description | | --- | --- | | Content-Type | Always \"application/json\". | | X-Time-Provisioning | The time taken to process the request (in ms). | | X-Api-Identity | The currently active Provisioning API version. Useful when reporting bugs to us. | | X-Request-Id   | The unique identifier of the request, be sure to include it when referring to a request. | | RateLimit-Limit | The number of requests that can be made per minute. | | RateLimit-Remaining | The number of requests that still remain before you hit your request limit. | | RateLimit-Reset | A [Unix timestamp](https://en.wikipedia.org/wiki/Unix_time) in milliseconds of when the rate limit will reset, or the time at which a request no longer will return 429 - Too Many Requests. |  ## Timestamp Format  All timestamps follow <a href=\"https://de.wikipedia.org/wiki/ISO_8601\" target=\"_blank_\">ISO 8601</a> and issued in <a href=\"https://www.timeanddate.de/zeitzonen/utc-gmt\" target=\"_blank_\">UTC</a>  ## CORS  ### Cross Origin Resource Sharing  To allow API access from other domains that supports the API CORS (Cross Origin Resource Sharing). See: enable-cors.org/ .  This allows direct use the API in the browser running a JavaScript web control panel.  All this is done in the background by the browser. The following HTTP headers are set by the API:  Header | Parameter | Description --- | --- | --- Access-Control-Allow-Methods   | GET, POST, PUT, PATCH, DELETE, OPTIONS | Contains all available methods that may be used for queries. Access-Control-Allow-Credentials | true | Is set to \"true\". Allows the browser to send the authentication data via X-Auth HTTP header. Access-Control-Allow-Headers | Origin, X-Requested-With, Content-Type, Accept, X-Auth-UserId, X-Auth-Token, X-Exec-Time, X-API-Version, X-Api-Client | The HTTP headers available for requests. Access-Control-Allow-Origin | * | The domain sent by the browser as a source of demand. Access-Control-Expose-Headers | X-Exec-Time, X-Api-Version | The HTTP headers that can be used by a browser application.  ## Rate Limits  The number of requests that can be made through our API is currently limited to 210 requests per 60 seconds. The current state of rate limiting is returned within the response headers of each request. The relevant response headers are  - RateLimit-Limit - RateLimit-Remaining - RateLimit-Reset  See the Response Headers section for details.  As long as the `RateLimit-Remaining` count is above zero, you will be able to make further requests. As soon as the `RateLimit-Remaining` header value is zero, subsequent requests will return the 429 status code. This will stay until the timestamp given in `RateLimit-Reset` has been reached.  ### Example rate limiting response  ```shell HTTP/1.0 429 TOO MANY REQUESTS Content-Length: 66 Content-Type: application/json; charset=utf-8 Date: Mon, 11 Nov 2019 11:11:33 GMT RateLimit-Limit: 210 RateLimit-Remaining: 0 RateLimit-Reset: 1573468299256  {     \"id\": \"too_many_requests\",     \"message\": \"API Rate limit exceeded.\" } ```  It is important to understand how rate limits are reset in order to use the API efficiently. Rate limits are reset for all counted requests at once. This means that that once the timestamp `RateLimit-Remaining` has arrived all counted request are reset and you can again start sending requests to the API.  This allows for short burst of traffic. The downside is once you have hit the request limit no more requests are allowed until the rate limit duration is reset.  ## Object Relations Relationships describe resource objects (storages, networks, IPs, etc.) that are connected to a server. These relationships are treated like objects themselves and can have properties specific to this relation.  One example would be, that the MAC address of a private network connected to a server (Server-to-Network relation) can be found as property of the relation itself - the relation is the _network interface_ in the server.  Another example is storage, where the SCSI LUN is also part of the Server-to-Storage relation object.  This information is especially interesting if some kind of network boot is used on the servers, where the properties of the server need to be known beforehand.  ## Deleted Objects Objects that are deleted are no longer visible on their *regular* endpoints. For historical reasons these objects are still available read-only on a special endpoint named /deleted. If objects have been deleted but have not yet been billed in the current period, the yet-to-be-billed price is still shown.  <!-- #strip_js --> ## Node.js Library  We have a JavaScript library for you to use our API with ease.  <a href=\"https://www.npmjs.com/package/@gridscale/api\" target=\"_blank\"><img src=\"https://badge.fury.io/js/%40gridscale%2Fapi.svg\" alt=\"npm badge\"></a>  <aside class=\"success\"> We want to make it even easier for you to manage your Infrastructure via our API - so feel free to contact us with any ideas, or languages you would like to see included. </aside>  Requests with our Node.js lib return a little differently. Everything is the same except it allows you to add URL parameters to customize your requests.  To get started <a href=\"https://www.npmjs.com/package/@gridscale/api\" target=\"_blank\">click here</a> .  <!-- #strip_js_end -->  <!-- #strip_go --> ## Golang Library We also have a Golang library for Gophers.  Requests with our Golang lib return a little differently. Everything is the same except it allows you to add URL parameters to customize your requests.  To get started <a href=\"https://github.com/gridscale/gsclient-go\" target=\"_blank\">click here</a> .  <!-- #strip_go_end -->  <!-- #strip_python --> ## Python Library  We have a Python library, that optionally also simplifies handling of asynchronous requests by mimicking synchronous blocking behaviour.  To get started <a href=\"https://pypi.org/project/gs-api-client/\" target=\"_blank\">click here</a> .  <!-- #strip_python_end -->  # Authentication  In order to use the API, the User-UUID and an API_Token are required. Both are available via the web GUI which can be found here on <a href=\"https://my.gridscale.io/APIs/\" target=\"_blank\">Your Account</a>  <aside class=\"success\"> If you are logged in, your UUID and Token will be pulled dynamically from your account, so you can copy request examples straight into your code. </aside>  The User-UUID remains the same, even if the users email address is changed. The API_Token is a randomly generated hash that allows read/write access.  ## API_Token  <table class=\"security-details\"><tbody><tr><th> Security scheme type: </th><td> API Key </td></tr><tr><th> header parameter name:</th><td> X-Auth-Token </td></tr></tbody></table>  ## User_UUID  <table class=\"security-details\"><tbody><tr><th> Security scheme type: </th><td> API Key </td></tr><tr><th> header parameter name:</th><td> X-Auth-UserId </td></tr></tbody></table>  ## Examples  <!-- #strip_js --> > Node.js ``` // to get started // read the docs @ https://www.npmjs.com/package/@gs_js_auth/api var gs_js_auth = require('@gs_js_auth/api').gs_js_auth; var client = new gs_js_auth.Client(\"##API_TOKEN##\",\"##USER_UUID##\"); ``` <!-- #strip_js_end -->  <!-- #strip_go --> > Golang ``` // to get started // read the docs @ https://github.com/gridscale/gsclient-go config := gsclient.NewConfiguration(   \"https://api.gridscale.io\",   \"##USER_UUID##\",   \"##API_TOKEN##\",   false, //set debug mode ) client := gsclient.NewClient(config) ``` <!-- #strip_go_end -->  > Shell Authentication Headers ```   -H \"X-Auth-UserId: ##USER_UUID##\" \\   -H \"X-Auth-Token: ##API_TOKEN##\" \\ ```  > Setting Authentication in your Environment variables ``` export API_TOKEN=\"##API_TOKEN##\" USER_UUID=\"##USER_UUID##\" ```  <aside class=\"notice\"> You must replace <code>USER_UUID</code> and <code>API_Token</code> with your personal UUID and API key respectively. </aside>   # noqa: E501

    OpenAPI spec version: 1.0.24
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from gs_api_client.swagger.models.task_events_server_server_add import TaskEventsServerServerAdd  # noqa: F401,E501
from gs_api_client.swagger.models.task_events_server_server_power_update import TaskEventsServerServerPowerUpdate  # noqa: F401,E501
from gs_api_client.swagger.models.task_events_server_server_relation_ipaddr_add import TaskEventsServerServerRelationIpaddrAdd  # noqa: F401,E501
from gs_api_client.swagger.models.task_events_server_server_relation_isoimage_add import TaskEventsServerServerRelationIsoimageAdd  # noqa: F401,E501
from gs_api_client.swagger.models.task_events_server_server_relation_isoimage_remove import TaskEventsServerServerRelationIsoimageRemove  # noqa: F401,E501
from gs_api_client.swagger.models.task_events_server_server_relation_network_add import TaskEventsServerServerRelationNetworkAdd  # noqa: F401,E501
from gs_api_client.swagger.models.task_events_server_server_relation_network_remove import TaskEventsServerServerRelationNetworkRemove  # noqa: F401,E501
from gs_api_client.swagger.models.task_events_server_server_relation_storage_add import TaskEventsServerServerRelationStorageAdd  # noqa: F401,E501
from gs_api_client.swagger.models.task_events_server_server_relation_storage_remove import TaskEventsServerServerRelationStorageRemove  # noqa: F401,E501
from gs_api_client.swagger.models.task_events_server_server_remove import TaskEventsServerServerRemove  # noqa: F401,E501
from gs_api_client.swagger.models.task_events_server_server_update import TaskEventsServerServerUpdate  # noqa: F401,E501


class TaskEventsServer(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'server_relation_isoimage_add': 'TaskEventsServerServerRelationIsoimageAdd',
        'server_relation_isoimage_update': 'TaskEventsServerServerRelationIsoimageAdd',
        'server_relation_isoimage_remove': 'TaskEventsServerServerRelationIsoimageRemove',
        'server_relation_ipaddr_add': 'TaskEventsServerServerRelationIpaddrAdd',
        'server_relation_ipaddr_remove': 'TaskEventsServerServerRelationIpaddrAdd',
        'server_relation_network_add': 'TaskEventsServerServerRelationNetworkAdd',
        'server_relation_network_update': 'TaskEventsServerServerRelationNetworkAdd',
        'server_relation_network_remove': 'TaskEventsServerServerRelationNetworkRemove',
        'server_relation_storage_add': 'TaskEventsServerServerRelationStorageAdd',
        'server_relation_storage_update': 'TaskEventsServerServerRelationStorageAdd',
        'server_relation_storage_remove': 'TaskEventsServerServerRelationStorageRemove',
        'server_add': 'TaskEventsServerServerAdd',
        'server_update': 'TaskEventsServerServerUpdate',
        'server_remove': 'TaskEventsServerServerRemove',
        'server_power_shutdown': 'TaskEventsServerServerRemove',
        'server_power_update': 'TaskEventsServerServerPowerUpdate'
    }

    attribute_map = {
        'server_relation_isoimage_add': 'server_relation_isoimage_add',
        'server_relation_isoimage_update': 'server_relation_isoimage_update',
        'server_relation_isoimage_remove': 'server_relation_isoimage_remove',
        'server_relation_ipaddr_add': 'server_relation_ipaddr_add',
        'server_relation_ipaddr_remove': 'server_relation_ipaddr_remove',
        'server_relation_network_add': 'server_relation_network_add',
        'server_relation_network_update': 'server_relation_network_update',
        'server_relation_network_remove': 'server_relation_network_remove',
        'server_relation_storage_add': 'server_relation_storage_add',
        'server_relation_storage_update': 'server_relation_storage_update',
        'server_relation_storage_remove': 'server_relation_storage_remove',
        'server_add': 'server_add',
        'server_update': 'server_update',
        'server_remove': 'server_remove',
        'server_power_shutdown': 'server_power_shutdown',
        'server_power_update': 'server_power_update'
    }

    def __init__(self, server_relation_isoimage_add=None, server_relation_isoimage_update=None, server_relation_isoimage_remove=None, server_relation_ipaddr_add=None, server_relation_ipaddr_remove=None, server_relation_network_add=None, server_relation_network_update=None, server_relation_network_remove=None, server_relation_storage_add=None, server_relation_storage_update=None, server_relation_storage_remove=None, server_add=None, server_update=None, server_remove=None, server_power_shutdown=None, server_power_update=None):  # noqa: E501
        """TaskEventsServer - a model defined in Swagger"""  # noqa: E501

        self._server_relation_isoimage_add = None
        self._server_relation_isoimage_update = None
        self._server_relation_isoimage_remove = None
        self._server_relation_ipaddr_add = None
        self._server_relation_ipaddr_remove = None
        self._server_relation_network_add = None
        self._server_relation_network_update = None
        self._server_relation_network_remove = None
        self._server_relation_storage_add = None
        self._server_relation_storage_update = None
        self._server_relation_storage_remove = None
        self._server_add = None
        self._server_update = None
        self._server_remove = None
        self._server_power_shutdown = None
        self._server_power_update = None
        self.discriminator = None

        if server_relation_isoimage_add is not None:
            self.server_relation_isoimage_add = server_relation_isoimage_add
        if server_relation_isoimage_update is not None:
            self.server_relation_isoimage_update = server_relation_isoimage_update
        if server_relation_isoimage_remove is not None:
            self.server_relation_isoimage_remove = server_relation_isoimage_remove
        if server_relation_ipaddr_add is not None:
            self.server_relation_ipaddr_add = server_relation_ipaddr_add
        if server_relation_ipaddr_remove is not None:
            self.server_relation_ipaddr_remove = server_relation_ipaddr_remove
        if server_relation_network_add is not None:
            self.server_relation_network_add = server_relation_network_add
        if server_relation_network_update is not None:
            self.server_relation_network_update = server_relation_network_update
        if server_relation_network_remove is not None:
            self.server_relation_network_remove = server_relation_network_remove
        if server_relation_storage_add is not None:
            self.server_relation_storage_add = server_relation_storage_add
        if server_relation_storage_update is not None:
            self.server_relation_storage_update = server_relation_storage_update
        if server_relation_storage_remove is not None:
            self.server_relation_storage_remove = server_relation_storage_remove
        if server_add is not None:
            self.server_add = server_add
        if server_update is not None:
            self.server_update = server_update
        if server_remove is not None:
            self.server_remove = server_remove
        if server_power_shutdown is not None:
            self.server_power_shutdown = server_power_shutdown
        if server_power_update is not None:
            self.server_power_update = server_power_update

    @property
    def server_relation_isoimage_add(self):
        """Gets the server_relation_isoimage_add of this TaskEventsServer.  # noqa: E501


        :return: The server_relation_isoimage_add of this TaskEventsServer.  # noqa: E501
        :rtype: TaskEventsServerServerRelationIsoimageAdd
        """
        return self._server_relation_isoimage_add

    @server_relation_isoimage_add.setter
    def server_relation_isoimage_add(self, server_relation_isoimage_add):
        """Sets the server_relation_isoimage_add of this TaskEventsServer.


        :param server_relation_isoimage_add: The server_relation_isoimage_add of this TaskEventsServer.  # noqa: E501
        :type: TaskEventsServerServerRelationIsoimageAdd
        """

        self._server_relation_isoimage_add = server_relation_isoimage_add

    @property
    def server_relation_isoimage_update(self):
        """Gets the server_relation_isoimage_update of this TaskEventsServer.  # noqa: E501


        :return: The server_relation_isoimage_update of this TaskEventsServer.  # noqa: E501
        :rtype: TaskEventsServerServerRelationIsoimageAdd
        """
        return self._server_relation_isoimage_update

    @server_relation_isoimage_update.setter
    def server_relation_isoimage_update(self, server_relation_isoimage_update):
        """Sets the server_relation_isoimage_update of this TaskEventsServer.


        :param server_relation_isoimage_update: The server_relation_isoimage_update of this TaskEventsServer.  # noqa: E501
        :type: TaskEventsServerServerRelationIsoimageAdd
        """

        self._server_relation_isoimage_update = server_relation_isoimage_update

    @property
    def server_relation_isoimage_remove(self):
        """Gets the server_relation_isoimage_remove of this TaskEventsServer.  # noqa: E501


        :return: The server_relation_isoimage_remove of this TaskEventsServer.  # noqa: E501
        :rtype: TaskEventsServerServerRelationIsoimageRemove
        """
        return self._server_relation_isoimage_remove

    @server_relation_isoimage_remove.setter
    def server_relation_isoimage_remove(self, server_relation_isoimage_remove):
        """Sets the server_relation_isoimage_remove of this TaskEventsServer.


        :param server_relation_isoimage_remove: The server_relation_isoimage_remove of this TaskEventsServer.  # noqa: E501
        :type: TaskEventsServerServerRelationIsoimageRemove
        """

        self._server_relation_isoimage_remove = server_relation_isoimage_remove

    @property
    def server_relation_ipaddr_add(self):
        """Gets the server_relation_ipaddr_add of this TaskEventsServer.  # noqa: E501


        :return: The server_relation_ipaddr_add of this TaskEventsServer.  # noqa: E501
        :rtype: TaskEventsServerServerRelationIpaddrAdd
        """
        return self._server_relation_ipaddr_add

    @server_relation_ipaddr_add.setter
    def server_relation_ipaddr_add(self, server_relation_ipaddr_add):
        """Sets the server_relation_ipaddr_add of this TaskEventsServer.


        :param server_relation_ipaddr_add: The server_relation_ipaddr_add of this TaskEventsServer.  # noqa: E501
        :type: TaskEventsServerServerRelationIpaddrAdd
        """

        self._server_relation_ipaddr_add = server_relation_ipaddr_add

    @property
    def server_relation_ipaddr_remove(self):
        """Gets the server_relation_ipaddr_remove of this TaskEventsServer.  # noqa: E501


        :return: The server_relation_ipaddr_remove of this TaskEventsServer.  # noqa: E501
        :rtype: TaskEventsServerServerRelationIpaddrAdd
        """
        return self._server_relation_ipaddr_remove

    @server_relation_ipaddr_remove.setter
    def server_relation_ipaddr_remove(self, server_relation_ipaddr_remove):
        """Sets the server_relation_ipaddr_remove of this TaskEventsServer.


        :param server_relation_ipaddr_remove: The server_relation_ipaddr_remove of this TaskEventsServer.  # noqa: E501
        :type: TaskEventsServerServerRelationIpaddrAdd
        """

        self._server_relation_ipaddr_remove = server_relation_ipaddr_remove

    @property
    def server_relation_network_add(self):
        """Gets the server_relation_network_add of this TaskEventsServer.  # noqa: E501


        :return: The server_relation_network_add of this TaskEventsServer.  # noqa: E501
        :rtype: TaskEventsServerServerRelationNetworkAdd
        """
        return self._server_relation_network_add

    @server_relation_network_add.setter
    def server_relation_network_add(self, server_relation_network_add):
        """Sets the server_relation_network_add of this TaskEventsServer.


        :param server_relation_network_add: The server_relation_network_add of this TaskEventsServer.  # noqa: E501
        :type: TaskEventsServerServerRelationNetworkAdd
        """

        self._server_relation_network_add = server_relation_network_add

    @property
    def server_relation_network_update(self):
        """Gets the server_relation_network_update of this TaskEventsServer.  # noqa: E501


        :return: The server_relation_network_update of this TaskEventsServer.  # noqa: E501
        :rtype: TaskEventsServerServerRelationNetworkAdd
        """
        return self._server_relation_network_update

    @server_relation_network_update.setter
    def server_relation_network_update(self, server_relation_network_update):
        """Sets the server_relation_network_update of this TaskEventsServer.


        :param server_relation_network_update: The server_relation_network_update of this TaskEventsServer.  # noqa: E501
        :type: TaskEventsServerServerRelationNetworkAdd
        """

        self._server_relation_network_update = server_relation_network_update

    @property
    def server_relation_network_remove(self):
        """Gets the server_relation_network_remove of this TaskEventsServer.  # noqa: E501


        :return: The server_relation_network_remove of this TaskEventsServer.  # noqa: E501
        :rtype: TaskEventsServerServerRelationNetworkRemove
        """
        return self._server_relation_network_remove

    @server_relation_network_remove.setter
    def server_relation_network_remove(self, server_relation_network_remove):
        """Sets the server_relation_network_remove of this TaskEventsServer.


        :param server_relation_network_remove: The server_relation_network_remove of this TaskEventsServer.  # noqa: E501
        :type: TaskEventsServerServerRelationNetworkRemove
        """

        self._server_relation_network_remove = server_relation_network_remove

    @property
    def server_relation_storage_add(self):
        """Gets the server_relation_storage_add of this TaskEventsServer.  # noqa: E501


        :return: The server_relation_storage_add of this TaskEventsServer.  # noqa: E501
        :rtype: TaskEventsServerServerRelationStorageAdd
        """
        return self._server_relation_storage_add

    @server_relation_storage_add.setter
    def server_relation_storage_add(self, server_relation_storage_add):
        """Sets the server_relation_storage_add of this TaskEventsServer.


        :param server_relation_storage_add: The server_relation_storage_add of this TaskEventsServer.  # noqa: E501
        :type: TaskEventsServerServerRelationStorageAdd
        """

        self._server_relation_storage_add = server_relation_storage_add

    @property
    def server_relation_storage_update(self):
        """Gets the server_relation_storage_update of this TaskEventsServer.  # noqa: E501


        :return: The server_relation_storage_update of this TaskEventsServer.  # noqa: E501
        :rtype: TaskEventsServerServerRelationStorageAdd
        """
        return self._server_relation_storage_update

    @server_relation_storage_update.setter
    def server_relation_storage_update(self, server_relation_storage_update):
        """Sets the server_relation_storage_update of this TaskEventsServer.


        :param server_relation_storage_update: The server_relation_storage_update of this TaskEventsServer.  # noqa: E501
        :type: TaskEventsServerServerRelationStorageAdd
        """

        self._server_relation_storage_update = server_relation_storage_update

    @property
    def server_relation_storage_remove(self):
        """Gets the server_relation_storage_remove of this TaskEventsServer.  # noqa: E501


        :return: The server_relation_storage_remove of this TaskEventsServer.  # noqa: E501
        :rtype: TaskEventsServerServerRelationStorageRemove
        """
        return self._server_relation_storage_remove

    @server_relation_storage_remove.setter
    def server_relation_storage_remove(self, server_relation_storage_remove):
        """Sets the server_relation_storage_remove of this TaskEventsServer.


        :param server_relation_storage_remove: The server_relation_storage_remove of this TaskEventsServer.  # noqa: E501
        :type: TaskEventsServerServerRelationStorageRemove
        """

        self._server_relation_storage_remove = server_relation_storage_remove

    @property
    def server_add(self):
        """Gets the server_add of this TaskEventsServer.  # noqa: E501


        :return: The server_add of this TaskEventsServer.  # noqa: E501
        :rtype: TaskEventsServerServerAdd
        """
        return self._server_add

    @server_add.setter
    def server_add(self, server_add):
        """Sets the server_add of this TaskEventsServer.


        :param server_add: The server_add of this TaskEventsServer.  # noqa: E501
        :type: TaskEventsServerServerAdd
        """

        self._server_add = server_add

    @property
    def server_update(self):
        """Gets the server_update of this TaskEventsServer.  # noqa: E501


        :return: The server_update of this TaskEventsServer.  # noqa: E501
        :rtype: TaskEventsServerServerUpdate
        """
        return self._server_update

    @server_update.setter
    def server_update(self, server_update):
        """Sets the server_update of this TaskEventsServer.


        :param server_update: The server_update of this TaskEventsServer.  # noqa: E501
        :type: TaskEventsServerServerUpdate
        """

        self._server_update = server_update

    @property
    def server_remove(self):
        """Gets the server_remove of this TaskEventsServer.  # noqa: E501


        :return: The server_remove of this TaskEventsServer.  # noqa: E501
        :rtype: TaskEventsServerServerRemove
        """
        return self._server_remove

    @server_remove.setter
    def server_remove(self, server_remove):
        """Sets the server_remove of this TaskEventsServer.


        :param server_remove: The server_remove of this TaskEventsServer.  # noqa: E501
        :type: TaskEventsServerServerRemove
        """

        self._server_remove = server_remove

    @property
    def server_power_shutdown(self):
        """Gets the server_power_shutdown of this TaskEventsServer.  # noqa: E501


        :return: The server_power_shutdown of this TaskEventsServer.  # noqa: E501
        :rtype: TaskEventsServerServerRemove
        """
        return self._server_power_shutdown

    @server_power_shutdown.setter
    def server_power_shutdown(self, server_power_shutdown):
        """Sets the server_power_shutdown of this TaskEventsServer.


        :param server_power_shutdown: The server_power_shutdown of this TaskEventsServer.  # noqa: E501
        :type: TaskEventsServerServerRemove
        """

        self._server_power_shutdown = server_power_shutdown

    @property
    def server_power_update(self):
        """Gets the server_power_update of this TaskEventsServer.  # noqa: E501


        :return: The server_power_update of this TaskEventsServer.  # noqa: E501
        :rtype: TaskEventsServerServerPowerUpdate
        """
        return self._server_power_update

    @server_power_update.setter
    def server_power_update(self, server_power_update):
        """Sets the server_power_update of this TaskEventsServer.


        :param server_power_update: The server_power_update of this TaskEventsServer.  # noqa: E501
        :type: TaskEventsServerServerPowerUpdate
        """

        self._server_power_update = server_power_update

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(TaskEventsServer, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, TaskEventsServer):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
