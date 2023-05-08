# coding: utf-8

"""
    API Specification

    # Introduction Welcome to the API documentation of gridscale.  A REST API is a programming interface that allows you to access and send data directly to our systems using HTTPS requests, without the need to use a web GUI. All the functionality you are already familiar with in your control panel is accessible through the API, including expert methods that are only available through the API. Allowing you to script any actions you require, regardless of their complexity.  First we will start with a general overview about how the API works, followed by an extensive list of each endpoint, describing them in great detail.  ## Requests  For security, gridscale requires all API requests are made through the HTTPS protocol so that traffic is encrypted. The following table displays the different type of requests that the interface responds to, depending on the action you require.  | Method | Description | | --- | --- | | GET | A simple search of information. The response is a JSON object. Requests using GET are always read-only. | | POST | Adds new objects and object relations. The POST request must contain all the required parameters in the form of a JSON object. | | PATCH | Changes an object or an object relation. The parameters in PATCH requests are usually optional, so only the changed parameters must be specified in a JSON object. | | DELETE | Deletes an object or object relation. The object is deleted if it exists. | | OPTIONS | Get an extensive list of the servers support methods and characteristics. We will not give example OPTION requests on each endpoint, as they are extensive and self-descriptive. |  <aside class=\"notice\"> The methods PATCH and DELETE are idempotent - that is, a request with identical parameters can be sent several times, and it doesn't change the result. </aside>  ## Status Codes  | HTTP Status | `Message` | Description | | --- | --- | --- | | 200 | `OK` | The request has been successfully processed and the result of the request is transmitted in the response. | | 202 | `Accepted` | The request has been accepted, but will run at a later date. Meaning we can not guarantee the success of the request. You should poll the request to be notified once the resource has been provisioned - see the requests endpoint on how to poll. | | 204 | `No Content` | The request was successful, but the answer deliberately contains no data. | | 400 | `Bad Request` | The request message was built incorrectly. | | 401 | `Unauthorised` | The request can not be performed without a valid authentication. X-Auth UserId or X-Auth token HTTP header is not set or the userID / token is invalid. | | 402 | `Payment Required` | Action can not be executed - not provided any or invalid payment methods. | | 403 | `Forbidden` | The request was not carried out due to lack of authorization of the user or because an impossible action was requested. | | 404 | `Not Found` | The requested resource was not found. Will also be used if you do a resource exists, but the user does not have permission for it. | | 405 | `Method Not Allowed` | The request may be made only with other HTTP methods (eg GET rather than POST). | | 409 | `Conflict` | The request was made under false assumptions. For example, a user can not be created twice with the same email. | | 415 | `Unsupported Media Type` | The contents of the request have been submitted with an invalid media type. All POST or PATCH requests must have \"Content-Type : application / json\" as a header, and send a JSON object as a payload. | | 416 | `Requested Range Not Satisfiable` | The request could not be fulfilled. It is possible that a resource limit was reached or an IPv4 address pool is exhausted. | | 424 | `Failed Dependency` | The request could not be performed because the object is in the wrong status. | | 429 | `Too Many Requests` | The request has been rejected because rate limits have been exceeded. |  <aside class=\"success\"> Status 200-204 indicates that the request has been accepted and is processed. </aside> <aside class=\"notice\"> Status 400-429 indicates that there was a problem with the request that originated on the client. You will find more information about the problem in the body of 4xx response. </aside> <aside class=\"warning\"> A status 500 means that there was a server-side problem and your request can not be processed now. </aside>  ## Request Headers  | Header | Description | | --- | --- | | Content-Type | Always \"application/json\". | | X-Auth-userId | The user UUID. This can be found in the panel under \"API\" and will never change ( even after the change of user e-mail). | | X-Auth-Token | Is generated from the API hash and must be sent with all API requests. Both the token and its permissions can be configured in the panel.|  ## Response Headers  | Header | Description | | --- | --- | | Content-Type | Always \"application/json\". | | X-Time-Provisioning | The time taken to process the request (in ms). | | X-Api-Identity | The currently active Provisioning API version. Useful when reporting bugs to us. | | X-Request-Id   | The unique identifier of the request, be sure to include it when referring to a request. | | RateLimit-Limit | The number of requests that can be made per minute. | | RateLimit-Remaining | The number of requests that still remain before you hit your request limit. | | RateLimit-Reset | A [Unix timestamp](https://en.wikipedia.org/wiki/Unix_time) in milliseconds of when the rate limit will reset, or the time at which a request no longer will return 429 - Too Many Requests. |  ## Timestamp Format  All timestamps follow <a href=\"https://de.wikipedia.org/wiki/ISO_8601\" target=\"_blank_\">ISO 8601</a> and issued in <a href=\"https://www.timeanddate.de/zeitzonen/utc-gmt\" target=\"_blank_\">UTC</a>  ## CORS  ### Cross Origin Resource Sharing  To allow API access from other domains that supports the API Cross Origin Resource Sharing (CORS). Read more about CORS [here](https://enable-cors.org/).  This allows direct use of the API in the browser running a JavaScript web control panel.  All this is done in the background by the browser. The following HTTP headers are set by the API:  Header | Parameter | Description --- | --- | --- Access-Control-Allow-Methods   | GET, POST, PUT, PATCH, DELETE, OPTIONS | Contains all available methods that may be used for queries. Access-Control-Allow-Credentials | true | Is set to \"true\". Allows the browser to send the authentication data via X-Auth HTTP header. Access-Control-Allow-Headers | Origin, X-Requested-With, Content-Type, Accept, X-Auth-UserId, X-Auth-Token, X-Exec-Time, X-API-Version, X-Api-Client | The HTTP headers available for requests. Access-Control-Allow-Origin | * | The domain sent by the browser as a source of demand. Access-Control-Expose-Headers | X-Exec-Time, X-Api-Version | The HTTP headers that can be used by a browser application.  ## Rate Limits  The number of requests that can be made through our API is currently limited to 210 requests per 60 seconds. The current state of rate limiting is returned within the response headers of each request. The relevant response headers are  - RateLimit-Limit - RateLimit-Remaining - RateLimit-Reset  See the Response Headers section for details.  As long as the `RateLimit-Remaining` count is above zero, you will be able to make further requests. As soon as the `RateLimit-Remaining` header value is zero, subsequent requests will return the 429 status code. This will stay until the timestamp given in `RateLimit-Reset` has been reached.  ### Example rate limiting response  ```shell HTTP/1.0 429 TOO MANY REQUESTS Content-Length: 66 Content-Type: application/json; charset=utf-8 Date: Mon, 11 Nov 2019 11:11:33 GMT RateLimit-Limit: 210 RateLimit-Remaining: 0 RateLimit-Reset: 1573468299256  {     \"id\": \"too_many_requests\",     \"message\": \"API Rate limit exceeded.\" } ```  It is important to understand how rate limits are reset in order to use the API efficiently. Rate limits are reset for all counted requests at once. This means that that once the timestamp `RateLimit-Remaining` has arrived all counted request are reset and you can again start sending requests to the API.  This allows for short burst of traffic. The downside is once you have hit the request limit no more requests are allowed until the rate limit duration is reset.  ## Object Relations Relationships describe resource objects (storages, networks, IPs, etc.) that are connected to a server. These relationships are treated like objects themselves and can have properties specific to this relation.  One example would be, that the MAC address of a private network connected to a server (Server-to-Network relation) can be found as property of the relation itself - the relation is the _network interface_ in the server.  Another example is storage, where the SCSI LUN is also part of the Server-to-Storage relation object.  This information is especially interesting if some kind of network boot is used on the servers, where the properties of the server need to be known beforehand.  ## Deleted Objects Objects that are deleted are no longer visible on their *regular* endpoints. For historical reasons these objects are still available read-only on a special endpoint named `/deleted`. If objects have been deleted but have not yet been billed in the current period, the yet-to-be-billed price is still shown.  <!-- #strip_js --> ## Node.js / Javascript Library  We have a JavaScript library for you to use our API with ease.  <a href=\"https://badge.fury.io/js/%40gridscale%2Fgsclient-js\"><img src=\"https://badge.fury.io/js/%40gridscale%2Fgsclient-js.svg\" alt=\"npm version\" height=\"18\"></a>  <aside class=\"success\"> We want to make it even easier for you to manage your Infrastructure via our API - so feel free to contact us with any ideas, or languages you would like to see included. </aside>  Requests with our Node.js lib return a little differently. Everything is the same except it allows you to add URL parameters to customize your requests.  To get started <a href=\"https://www.npmjs.com/package/@gridscale/gsclient-js\" target=\"_blank\">click here</a> .  <!-- #strip_js_end -->  <!-- #strip_go --> ## Golang Library We also have a Golang library for Gophers.  Requests with our Golang lib return a little differently. Everything is the same except it allows you to add URL parameters to customize your requests.  To get started <a href=\"https://github.com/gridscale/gsclient-go\" target=\"_blank\">click here</a> .  <!-- #strip_go_end -->  <!-- #strip_python --> ## Python Library  We have a Python library, that optionally also simplifies handling of asynchronous requests by mimicking synchronous blocking behaviour.  To get started <a href=\"https://pypi.org/project/gs-api-client/\" target=\"_blank\">click here</a> .  <!-- #strip_python_end -->  # Authentication  In order to use the API, the User-UUID and an API_Token are required. Both are available via the web GUI which can be found here on <a href=\"https://my.gridscale.io/APIKey/\" target=\"_blank\">Your Account</a>  <aside class=\"success\"> If you are logged in, your UUID and Token will be pulled dynamically from your account, so you can copy request examples straight into your code. </aside>  The User-UUID remains the same, even if the users email address is changed. The API_Token is a randomly generated hash that allows read/write access.  ## API_Token  <table class=\"security-details\"><tbody><tr><th> Security scheme type: </th><td> API Key </td></tr><tr><th> header parameter name:</th><td> X-Auth-Token </td></tr></tbody></table>  ## User_UUID  <table class=\"security-details\"><tbody><tr><th> Security scheme type: </th><td> API Key </td></tr><tr><th> header parameter name:</th><td> X-Auth-UserId </td></tr></tbody></table>  ## Examples  <!-- #strip_js --> > Node.js ``` // to get started // read the docs @ https://www.npmjs.com/package/@gs_js_auth/api var gs_js_auth = require('@gs_js_auth/api').gs_js_auth; var client = new gs_js_auth.Client(\"##API_TOKEN##\",\"##USER_UUID##\"); ``` <!-- #strip_js_end -->  <!-- #strip_go --> > Golang ``` // to get started // read the docs @ https://github.com/gridscale/gsclient-go config := gsclient.NewConfiguration(   \"https://api.gridscale.io\",   \"##USER_UUID##\",   \"##API_TOKEN##\",   false, //set debug mode ) client := gsclient.NewClient(config) ``` <!-- #strip_go_end -->  > Shell Authentication Headers ```   -H \"X-Auth-UserId: ##USER_UUID##\" \\   -H \"X-Auth-Token: ##API_TOKEN##\" \\ ```  > Setting Authentication in your Environment variables ``` export API_TOKEN=\"##API_TOKEN##\" USER_UUID=\"##USER_UUID##\" ```  <aside class=\"notice\"> You must replace <code>USER_UUID</code> and <code>API_Token</code> with your personal UUID and API key respectively. </aside>   # noqa: E501

    OpenAPI spec version: 1.0.77
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from gs_api_client.swagger.models.accumulated_usage import AccumulatedUsage  # noqa: F401,E501
from gs_api_client.swagger.models.current_usage_per_minute import CurrentUsagePerMinute  # noqa: F401,E501
from gs_api_client.swagger.models.server_hardware_profile_config import ServerHardwareProfileConfig  # noqa: F401,E501
from gs_api_client.swagger.models.server_relation import ServerRelation  # noqa: F401,E501


class Server(object):
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
        'cores': 'int',
        'relations': 'ServerRelation',
        'legacy': 'bool',
        'memory': 'int',
        'console_token': 'str',
        'usage_in_minutes_memory': 'int',
        'auto_recovery': 'bool',
        'create_time': 'datetime',
        'current_price': 'float',
        'current_usage_per_minute': 'CurrentUsagePerMinute',
        'accumulated_usage': 'AccumulatedUsage',
        'location_country': 'str',
        'location_uuid': 'str',
        'usage_in_minutes_cores': 'int',
        'object_uuid': 'str',
        'change_time': 'datetime',
        'availability_zone': 'str',
        'location_iata': 'str',
        'labels': 'list[str]',
        'hardware_profile': 'str',
        'location_name': 'str',
        'power': 'bool',
        'name': 'str',
        'status': 'str',
        'hardware_profile_config': 'ServerHardwareProfileConfig',
        'user_data': 'str'
    }

    attribute_map = {
        'cores': 'cores',
        'relations': 'relations',
        'legacy': 'legacy',
        'memory': 'memory',
        'console_token': 'console_token',
        'usage_in_minutes_memory': 'usage_in_minutes_memory',
        'auto_recovery': 'auto_recovery',
        'create_time': 'create_time',
        'current_price': 'current_price',
        'current_usage_per_minute': 'current_usage_per_minute',
        'accumulated_usage': 'accumulated_usage',
        'location_country': 'location_country',
        'location_uuid': 'location_uuid',
        'usage_in_minutes_cores': 'usage_in_minutes_cores',
        'object_uuid': 'object_uuid',
        'change_time': 'change_time',
        'availability_zone': 'availability_zone',
        'location_iata': 'location_iata',
        'labels': 'labels',
        'hardware_profile': 'hardware_profile',
        'location_name': 'location_name',
        'power': 'power',
        'name': 'name',
        'status': 'status',
        'hardware_profile_config': 'hardware_profile_config',
        'user_data': 'user_data'
    }

    def __init__(self, cores=None, relations=None, legacy=None, memory=None, console_token=None, usage_in_minutes_memory=None, auto_recovery=None, create_time=None, current_price=None, current_usage_per_minute=None, accumulated_usage=None, location_country=None, location_uuid=None, usage_in_minutes_cores=None, object_uuid=None, change_time=None, availability_zone=None, location_iata=None, labels=None, hardware_profile=None, location_name=None, power=None, name=None, status=None, hardware_profile_config=None, user_data=None):  # noqa: E501
        """Server - a model defined in Swagger"""  # noqa: E501

        self._cores = None
        self._relations = None
        self._legacy = None
        self._memory = None
        self._console_token = None
        self._usage_in_minutes_memory = None
        self._auto_recovery = None
        self._create_time = None
        self._current_price = None
        self._current_usage_per_minute = None
        self._accumulated_usage = None
        self._location_country = None
        self._location_uuid = None
        self._usage_in_minutes_cores = None
        self._object_uuid = None
        self._change_time = None
        self._availability_zone = None
        self._location_iata = None
        self._labels = None
        self._hardware_profile = None
        self._location_name = None
        self._power = None
        self._name = None
        self._status = None
        self._hardware_profile_config = None
        self._user_data = None
        self.discriminator = None

        if cores is not None:
            self.cores = cores
        if relations is not None:
            self.relations = relations
        if legacy is not None:
            self.legacy = legacy
        if memory is not None:
            self.memory = memory
        if console_token is not None:
            self.console_token = console_token
        if usage_in_minutes_memory is not None:
            self.usage_in_minutes_memory = usage_in_minutes_memory
        if auto_recovery is not None:
            self.auto_recovery = auto_recovery
        if create_time is not None:
            self.create_time = create_time
        if current_price is not None:
            self.current_price = current_price
        if current_usage_per_minute is not None:
            self.current_usage_per_minute = current_usage_per_minute
        if accumulated_usage is not None:
            self.accumulated_usage = accumulated_usage
        if location_country is not None:
            self.location_country = location_country
        if location_uuid is not None:
            self.location_uuid = location_uuid
        if usage_in_minutes_cores is not None:
            self.usage_in_minutes_cores = usage_in_minutes_cores
        if object_uuid is not None:
            self.object_uuid = object_uuid
        if change_time is not None:
            self.change_time = change_time
        if availability_zone is not None:
            self.availability_zone = availability_zone
        if location_iata is not None:
            self.location_iata = location_iata
        if labels is not None:
            self.labels = labels
        if hardware_profile is not None:
            self.hardware_profile = hardware_profile
        if location_name is not None:
            self.location_name = location_name
        if power is not None:
            self.power = power
        if name is not None:
            self.name = name
        if status is not None:
            self.status = status
        if hardware_profile_config is not None:
            self.hardware_profile_config = hardware_profile_config
        if user_data is not None:
            self.user_data = user_data

    @property
    def cores(self):
        """Gets the cores of this Server.  # noqa: E501

        Number of server cores.  # noqa: E501

        :return: The cores of this Server.  # noqa: E501
        :rtype: int
        """
        return self._cores

    @cores.setter
    def cores(self, cores):
        """Sets the cores of this Server.

        Number of server cores.  # noqa: E501

        :param cores: The cores of this Server.  # noqa: E501
        :type: int
        """

        self._cores = cores

    @property
    def relations(self):
        """Gets the relations of this Server.  # noqa: E501


        :return: The relations of this Server.  # noqa: E501
        :rtype: ServerRelation
        """
        return self._relations

    @relations.setter
    def relations(self, relations):
        """Sets the relations of this Server.


        :param relations: The relations of this Server.  # noqa: E501
        :type: ServerRelation
        """

        self._relations = relations

    @property
    def legacy(self):
        """Gets the legacy of this Server.  # noqa: E501

        Legacy-Hardware emulation instead of virtio hardware. If enabled, hotplugging cores, memory, storage, network, etc. will not work, but the server will most likely run every x86 compatible operating system. This mode comes with a performance penalty, as emulated hardware does not benefit from the virtio driver infrastructure.  # noqa: E501

        :return: The legacy of this Server.  # noqa: E501
        :rtype: bool
        """
        return self._legacy

    @legacy.setter
    def legacy(self, legacy):
        """Sets the legacy of this Server.

        Legacy-Hardware emulation instead of virtio hardware. If enabled, hotplugging cores, memory, storage, network, etc. will not work, but the server will most likely run every x86 compatible operating system. This mode comes with a performance penalty, as emulated hardware does not benefit from the virtio driver infrastructure.  # noqa: E501

        :param legacy: The legacy of this Server.  # noqa: E501
        :type: bool
        """

        self._legacy = legacy

    @property
    def memory(self):
        """Gets the memory of this Server.  # noqa: E501

        Indicates the amount of memory in GB.  # noqa: E501

        :return: The memory of this Server.  # noqa: E501
        :rtype: int
        """
        return self._memory

    @memory.setter
    def memory(self, memory):
        """Sets the memory of this Server.

        Indicates the amount of memory in GB.  # noqa: E501

        :param memory: The memory of this Server.  # noqa: E501
        :type: int
        """

        self._memory = memory

    @property
    def console_token(self):
        """Gets the console_token of this Server.  # noqa: E501

        The token used by the panel to open the websocket VNC connection to the server console.  # noqa: E501

        :return: The console_token of this Server.  # noqa: E501
        :rtype: str
        """
        return self._console_token

    @console_token.setter
    def console_token(self, console_token):
        """Sets the console_token of this Server.

        The token used by the panel to open the websocket VNC connection to the server console.  # noqa: E501

        :param console_token: The console_token of this Server.  # noqa: E501
        :type: str
        """

        self._console_token = console_token

    @property
    def usage_in_minutes_memory(self):
        """Gets the usage_in_minutes_memory of this Server.  # noqa: E501

        Total minutes of memory used.  # noqa: E501

        :return: The usage_in_minutes_memory of this Server.  # noqa: E501
        :rtype: int
        """
        return self._usage_in_minutes_memory

    @usage_in_minutes_memory.setter
    def usage_in_minutes_memory(self, usage_in_minutes_memory):
        """Sets the usage_in_minutes_memory of this Server.

        Total minutes of memory used.  # noqa: E501

        :param usage_in_minutes_memory: The usage_in_minutes_memory of this Server.  # noqa: E501
        :type: int
        """

        self._usage_in_minutes_memory = usage_in_minutes_memory

    @property
    def auto_recovery(self):
        """Gets the auto_recovery of this Server.  # noqa: E501

        If the server should be auto-started in case of a failure (default=true).  # noqa: E501

        :return: The auto_recovery of this Server.  # noqa: E501
        :rtype: bool
        """
        return self._auto_recovery

    @auto_recovery.setter
    def auto_recovery(self, auto_recovery):
        """Sets the auto_recovery of this Server.

        If the server should be auto-started in case of a failure (default=true).  # noqa: E501

        :param auto_recovery: The auto_recovery of this Server.  # noqa: E501
        :type: bool
        """

        self._auto_recovery = auto_recovery

    @property
    def create_time(self):
        """Gets the create_time of this Server.  # noqa: E501

        Defines the date and time the object was initially created.  # noqa: E501

        :return: The create_time of this Server.  # noqa: E501
        :rtype: datetime
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this Server.

        Defines the date and time the object was initially created.  # noqa: E501

        :param create_time: The create_time of this Server.  # noqa: E501
        :type: datetime
        """

        self._create_time = create_time

    @property
    def current_price(self):
        """Gets the current_price of this Server.  # noqa: E501

        Deprecated  # noqa: E501

        :return: The current_price of this Server.  # noqa: E501
        :rtype: float
        """
        return self._current_price

    @current_price.setter
    def current_price(self, current_price):
        """Sets the current_price of this Server.

        Deprecated  # noqa: E501

        :param current_price: The current_price of this Server.  # noqa: E501
        :type: float
        """

        self._current_price = current_price

    @property
    def current_usage_per_minute(self):
        """Gets the current_usage_per_minute of this Server.  # noqa: E501


        :return: The current_usage_per_minute of this Server.  # noqa: E501
        :rtype: CurrentUsagePerMinute
        """
        return self._current_usage_per_minute

    @current_usage_per_minute.setter
    def current_usage_per_minute(self, current_usage_per_minute):
        """Sets the current_usage_per_minute of this Server.


        :param current_usage_per_minute: The current_usage_per_minute of this Server.  # noqa: E501
        :type: CurrentUsagePerMinute
        """

        self._current_usage_per_minute = current_usage_per_minute

    @property
    def accumulated_usage(self):
        """Gets the accumulated_usage of this Server.  # noqa: E501


        :return: The accumulated_usage of this Server.  # noqa: E501
        :rtype: AccumulatedUsage
        """
        return self._accumulated_usage

    @accumulated_usage.setter
    def accumulated_usage(self, accumulated_usage):
        """Sets the accumulated_usage of this Server.


        :param accumulated_usage: The accumulated_usage of this Server.  # noqa: E501
        :type: AccumulatedUsage
        """

        self._accumulated_usage = accumulated_usage

    @property
    def location_country(self):
        """Gets the location_country of this Server.  # noqa: E501

        The human-readable name of the location. It supports the full UTF-8 character set, with a maximum of 64 characters.  # noqa: E501

        :return: The location_country of this Server.  # noqa: E501
        :rtype: str
        """
        return self._location_country

    @location_country.setter
    def location_country(self, location_country):
        """Sets the location_country of this Server.

        The human-readable name of the location. It supports the full UTF-8 character set, with a maximum of 64 characters.  # noqa: E501

        :param location_country: The location_country of this Server.  # noqa: E501
        :type: str
        """

        self._location_country = location_country

    @property
    def location_uuid(self):
        """Gets the location_uuid of this Server.  # noqa: E501

        Helps to identify which data-center an object belongs to.  # noqa: E501

        :return: The location_uuid of this Server.  # noqa: E501
        :rtype: str
        """
        return self._location_uuid

    @location_uuid.setter
    def location_uuid(self, location_uuid):
        """Sets the location_uuid of this Server.

        Helps to identify which data-center an object belongs to.  # noqa: E501

        :param location_uuid: The location_uuid of this Server.  # noqa: E501
        :type: str
        """

        self._location_uuid = location_uuid

    @property
    def usage_in_minutes_cores(self):
        """Gets the usage_in_minutes_cores of this Server.  # noqa: E501

        Total minutes of cores used.  # noqa: E501

        :return: The usage_in_minutes_cores of this Server.  # noqa: E501
        :rtype: int
        """
        return self._usage_in_minutes_cores

    @usage_in_minutes_cores.setter
    def usage_in_minutes_cores(self, usage_in_minutes_cores):
        """Sets the usage_in_minutes_cores of this Server.

        Total minutes of cores used.  # noqa: E501

        :param usage_in_minutes_cores: The usage_in_minutes_cores of this Server.  # noqa: E501
        :type: int
        """

        self._usage_in_minutes_cores = usage_in_minutes_cores

    @property
    def object_uuid(self):
        """Gets the object_uuid of this Server.  # noqa: E501

        The UUID of an object is always unique, and refers to a specific object.  # noqa: E501

        :return: The object_uuid of this Server.  # noqa: E501
        :rtype: str
        """
        return self._object_uuid

    @object_uuid.setter
    def object_uuid(self, object_uuid):
        """Sets the object_uuid of this Server.

        The UUID of an object is always unique, and refers to a specific object.  # noqa: E501

        :param object_uuid: The object_uuid of this Server.  # noqa: E501
        :type: str
        """

        self._object_uuid = object_uuid

    @property
    def change_time(self):
        """Gets the change_time of this Server.  # noqa: E501

        Defines the date and time of the last object change.  # noqa: E501

        :return: The change_time of this Server.  # noqa: E501
        :rtype: datetime
        """
        return self._change_time

    @change_time.setter
    def change_time(self, change_time):
        """Sets the change_time of this Server.

        Defines the date and time of the last object change.  # noqa: E501

        :param change_time: The change_time of this Server.  # noqa: E501
        :type: datetime
        """

        self._change_time = change_time

    @property
    def availability_zone(self):
        """Gets the availability_zone of this Server.  # noqa: E501

        Which Availability-Zone the Server is placed.  # noqa: E501

        :return: The availability_zone of this Server.  # noqa: E501
        :rtype: str
        """
        return self._availability_zone

    @availability_zone.setter
    def availability_zone(self, availability_zone):
        """Sets the availability_zone of this Server.

        Which Availability-Zone the Server is placed.  # noqa: E501

        :param availability_zone: The availability_zone of this Server.  # noqa: E501
        :type: str
        """

        self._availability_zone = availability_zone

    @property
    def location_iata(self):
        """Gets the location_iata of this Server.  # noqa: E501

        Uses IATA airport code, which works as a location identifier.  # noqa: E501

        :return: The location_iata of this Server.  # noqa: E501
        :rtype: str
        """
        return self._location_iata

    @location_iata.setter
    def location_iata(self, location_iata):
        """Sets the location_iata of this Server.

        Uses IATA airport code, which works as a location identifier.  # noqa: E501

        :param location_iata: The location_iata of this Server.  # noqa: E501
        :type: str
        """

        self._location_iata = location_iata

    @property
    def labels(self):
        """Gets the labels of this Server.  # noqa: E501

        List of labels.  # noqa: E501

        :return: The labels of this Server.  # noqa: E501
        :rtype: list[str]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this Server.

        List of labels.  # noqa: E501

        :param labels: The labels of this Server.  # noqa: E501
        :type: list[str]
        """

        self._labels = labels

    @property
    def hardware_profile(self):
        """Gets the hardware_profile of this Server.  # noqa: E501

        Specifies the hardware settings for the virtual machine.  # noqa: E501

        :return: The hardware_profile of this Server.  # noqa: E501
        :rtype: str
        """
        return self._hardware_profile

    @hardware_profile.setter
    def hardware_profile(self, hardware_profile):
        """Sets the hardware_profile of this Server.

        Specifies the hardware settings for the virtual machine.  # noqa: E501

        :param hardware_profile: The hardware_profile of this Server.  # noqa: E501
        :type: str
        """

        self._hardware_profile = hardware_profile

    @property
    def location_name(self):
        """Gets the location_name of this Server.  # noqa: E501

        The human-readable name of the location. It supports the full UTF-8 character set, with a maximum of 64 characters.  # noqa: E501

        :return: The location_name of this Server.  # noqa: E501
        :rtype: str
        """
        return self._location_name

    @location_name.setter
    def location_name(self, location_name):
        """Sets the location_name of this Server.

        The human-readable name of the location. It supports the full UTF-8 character set, with a maximum of 64 characters.  # noqa: E501

        :param location_name: The location_name of this Server.  # noqa: E501
        :type: str
        """

        self._location_name = location_name

    @property
    def power(self):
        """Gets the power of this Server.  # noqa: E501

        The power status of the server.  # noqa: E501

        :return: The power of this Server.  # noqa: E501
        :rtype: bool
        """
        return self._power

    @power.setter
    def power(self, power):
        """Sets the power of this Server.

        The power status of the server.  # noqa: E501

        :param power: The power of this Server.  # noqa: E501
        :type: bool
        """

        self._power = power

    @property
    def name(self):
        """Gets the name of this Server.  # noqa: E501

        The human-readable name of the object. It supports the full UTF-8 character set, with a maximum of 64 characters.  # noqa: E501

        :return: The name of this Server.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Server.

        The human-readable name of the object. It supports the full UTF-8 character set, with a maximum of 64 characters.  # noqa: E501

        :param name: The name of this Server.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def status(self):
        """Gets the status of this Server.  # noqa: E501

        Status indicates the status of the object, e.g., in-provisioning or active.  # noqa: E501

        :return: The status of this Server.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Server.

        Status indicates the status of the object, e.g., in-provisioning or active.  # noqa: E501

        :param status: The status of this Server.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def hardware_profile_config(self):
        """Gets the hardware_profile_config of this Server.  # noqa: E501


        :return: The hardware_profile_config of this Server.  # noqa: E501
        :rtype: ServerHardwareProfileConfig
        """
        return self._hardware_profile_config

    @hardware_profile_config.setter
    def hardware_profile_config(self, hardware_profile_config):
        """Sets the hardware_profile_config of this Server.


        :param hardware_profile_config: The hardware_profile_config of this Server.  # noqa: E501
        :type: ServerHardwareProfileConfig
        """

        self._hardware_profile_config = hardware_profile_config

    @property
    def user_data(self):
        """Gets the user_data of this Server.  # noqa: E501

        For system configuration on first boot. May contain cloud-config data or shell scripting, encoded as base64 string. Supported tools are cloud-init, Cloudbase-init, and Ignition.  # noqa: E501

        :return: The user_data of this Server.  # noqa: E501
        :rtype: str
        """
        return self._user_data

    @user_data.setter
    def user_data(self, user_data):
        """Sets the user_data of this Server.

        For system configuration on first boot. May contain cloud-config data or shell scripting, encoded as base64 string. Supported tools are cloud-init, Cloudbase-init, and Ignition.  # noqa: E501

        :param user_data: The user_data of this Server.  # noqa: E501
        :type: str
        """
        if user_data is not None and not re.search(r'^(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$', user_data):  # noqa: E501
            raise ValueError(r"Invalid value for `user_data`, must be a follow pattern or equal to `/^(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$/`")  # noqa: E501

        self._user_data = user_data

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
        if issubclass(Server, dict):
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
        if not isinstance(other, Server):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
