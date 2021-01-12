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

from gs_api_client.swagger.models.ip_relation import IpRelation  # noqa: F401,E501


class Ip(object):
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
        'create_time': 'datetime',
        'status': 'str',
        'relations': 'IpRelation',
        'object_uuid': 'str',
        'location_country': 'str',
        'prefix': 'str',
        'delete_block': 'bool',
        'failover': 'bool',
        'location_uuid': 'str',
        'location_name': 'str',
        'labels': 'list[str]',
        'change_time': 'datetime',
        'ip': 'str',
        'family': 'str',
        'location_iata': 'str',
        'reverse_dns': 'str',
        'current_price': 'float',
        'usage_in_minutes': 'int',
        'name': 'str'
    }

    attribute_map = {
        'create_time': 'create_time',
        'status': 'status',
        'relations': 'relations',
        'object_uuid': 'object_uuid',
        'location_country': 'location_country',
        'prefix': 'prefix',
        'delete_block': 'delete_block',
        'failover': 'failover',
        'location_uuid': 'location_uuid',
        'location_name': 'location_name',
        'labels': 'labels',
        'change_time': 'change_time',
        'ip': 'ip',
        'family': 'family',
        'location_iata': 'location_iata',
        'reverse_dns': 'reverse_dns',
        'current_price': 'current_price',
        'usage_in_minutes': 'usage_in_minutes',
        'name': 'name'
    }

    def __init__(self, create_time=None, status=None, relations=None, object_uuid=None, location_country=None, prefix=None, delete_block=None, failover=None, location_uuid=None, location_name=None, labels=None, change_time=None, ip=None, family=None, location_iata=None, reverse_dns=None, current_price=None, usage_in_minutes=None, name=None):  # noqa: E501
        """Ip - a model defined in Swagger"""  # noqa: E501

        self._create_time = None
        self._status = None
        self._relations = None
        self._object_uuid = None
        self._location_country = None
        self._prefix = None
        self._delete_block = None
        self._failover = None
        self._location_uuid = None
        self._location_name = None
        self._labels = None
        self._change_time = None
        self._ip = None
        self._family = None
        self._location_iata = None
        self._reverse_dns = None
        self._current_price = None
        self._usage_in_minutes = None
        self._name = None
        self.discriminator = None

        if create_time is not None:
            self.create_time = create_time
        if status is not None:
            self.status = status
        if relations is not None:
            self.relations = relations
        if object_uuid is not None:
            self.object_uuid = object_uuid
        if location_country is not None:
            self.location_country = location_country
        if prefix is not None:
            self.prefix = prefix
        if delete_block is not None:
            self.delete_block = delete_block
        if failover is not None:
            self.failover = failover
        if location_uuid is not None:
            self.location_uuid = location_uuid
        if location_name is not None:
            self.location_name = location_name
        if labels is not None:
            self.labels = labels
        if change_time is not None:
            self.change_time = change_time
        if ip is not None:
            self.ip = ip
        if family is not None:
            self.family = family
        if location_iata is not None:
            self.location_iata = location_iata
        if reverse_dns is not None:
            self.reverse_dns = reverse_dns
        if current_price is not None:
            self.current_price = current_price
        if usage_in_minutes is not None:
            self.usage_in_minutes = usage_in_minutes
        if name is not None:
            self.name = name

    @property
    def create_time(self):
        """Gets the create_time of this Ip.  # noqa: E501

        Defines the date and time the object was initially created.  # noqa: E501

        :return: The create_time of this Ip.  # noqa: E501
        :rtype: datetime
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this Ip.

        Defines the date and time the object was initially created.  # noqa: E501

        :param create_time: The create_time of this Ip.  # noqa: E501
        :type: datetime
        """

        self._create_time = create_time

    @property
    def status(self):
        """Gets the status of this Ip.  # noqa: E501

        Status indicates the status of the object.  # noqa: E501

        :return: The status of this Ip.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Ip.

        Status indicates the status of the object.  # noqa: E501

        :param status: The status of this Ip.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def relations(self):
        """Gets the relations of this Ip.  # noqa: E501


        :return: The relations of this Ip.  # noqa: E501
        :rtype: IpRelation
        """
        return self._relations

    @relations.setter
    def relations(self, relations):
        """Sets the relations of this Ip.


        :param relations: The relations of this Ip.  # noqa: E501
        :type: IpRelation
        """

        self._relations = relations

    @property
    def object_uuid(self):
        """Gets the object_uuid of this Ip.  # noqa: E501

        The UUID of an object is always unique, and refers to a specific object.  # noqa: E501

        :return: The object_uuid of this Ip.  # noqa: E501
        :rtype: str
        """
        return self._object_uuid

    @object_uuid.setter
    def object_uuid(self, object_uuid):
        """Sets the object_uuid of this Ip.

        The UUID of an object is always unique, and refers to a specific object.  # noqa: E501

        :param object_uuid: The object_uuid of this Ip.  # noqa: E501
        :type: str
        """

        self._object_uuid = object_uuid

    @property
    def location_country(self):
        """Gets the location_country of this Ip.  # noqa: E501

        The human-readable name of the location. It supports the full UTF-8 character set, with a maximum of 64 characters.  # noqa: E501

        :return: The location_country of this Ip.  # noqa: E501
        :rtype: str
        """
        return self._location_country

    @location_country.setter
    def location_country(self, location_country):
        """Sets the location_country of this Ip.

        The human-readable name of the location. It supports the full UTF-8 character set, with a maximum of 64 characters.  # noqa: E501

        :param location_country: The location_country of this Ip.  # noqa: E501
        :type: str
        """

        self._location_country = location_country

    @property
    def prefix(self):
        """Gets the prefix of this Ip.  # noqa: E501

        The IP prefix.  # noqa: E501

        :return: The prefix of this Ip.  # noqa: E501
        :rtype: str
        """
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        """Sets the prefix of this Ip.

        The IP prefix.  # noqa: E501

        :param prefix: The prefix of this Ip.  # noqa: E501
        :type: str
        """

        self._prefix = prefix

    @property
    def delete_block(self):
        """Gets the delete_block of this Ip.  # noqa: E501

        Defines if the object is administratively blocked. If true, it can not be deleted by the user.  # noqa: E501

        :return: The delete_block of this Ip.  # noqa: E501
        :rtype: bool
        """
        return self._delete_block

    @delete_block.setter
    def delete_block(self, delete_block):
        """Sets the delete_block of this Ip.

        Defines if the object is administratively blocked. If true, it can not be deleted by the user.  # noqa: E501

        :param delete_block: The delete_block of this Ip.  # noqa: E501
        :type: bool
        """

        self._delete_block = delete_block

    @property
    def failover(self):
        """Gets the failover of this Ip.  # noqa: E501

        Sets failover mode for this IP. If true, then this IP is no longer available for DHCP and can no longer be related to any server.  # noqa: E501

        :return: The failover of this Ip.  # noqa: E501
        :rtype: bool
        """
        return self._failover

    @failover.setter
    def failover(self, failover):
        """Sets the failover of this Ip.

        Sets failover mode for this IP. If true, then this IP is no longer available for DHCP and can no longer be related to any server.  # noqa: E501

        :param failover: The failover of this Ip.  # noqa: E501
        :type: bool
        """

        self._failover = failover

    @property
    def location_uuid(self):
        """Gets the location_uuid of this Ip.  # noqa: E501

        Helps to identify which data-center an object belongs to.  # noqa: E501

        :return: The location_uuid of this Ip.  # noqa: E501
        :rtype: str
        """
        return self._location_uuid

    @location_uuid.setter
    def location_uuid(self, location_uuid):
        """Sets the location_uuid of this Ip.

        Helps to identify which data-center an object belongs to.  # noqa: E501

        :param location_uuid: The location_uuid of this Ip.  # noqa: E501
        :type: str
        """

        self._location_uuid = location_uuid

    @property
    def location_name(self):
        """Gets the location_name of this Ip.  # noqa: E501

        The human-readable name of the location. It supports the full UTF-8 character set, with a maximum of 64 characters.  # noqa: E501

        :return: The location_name of this Ip.  # noqa: E501
        :rtype: str
        """
        return self._location_name

    @location_name.setter
    def location_name(self, location_name):
        """Sets the location_name of this Ip.

        The human-readable name of the location. It supports the full UTF-8 character set, with a maximum of 64 characters.  # noqa: E501

        :param location_name: The location_name of this Ip.  # noqa: E501
        :type: str
        """

        self._location_name = location_name

    @property
    def labels(self):
        """Gets the labels of this Ip.  # noqa: E501

        List of labels.  # noqa: E501

        :return: The labels of this Ip.  # noqa: E501
        :rtype: list[str]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this Ip.

        List of labels.  # noqa: E501

        :param labels: The labels of this Ip.  # noqa: E501
        :type: list[str]
        """

        self._labels = labels

    @property
    def change_time(self):
        """Gets the change_time of this Ip.  # noqa: E501

        Defines the date and time of the last object change.  # noqa: E501

        :return: The change_time of this Ip.  # noqa: E501
        :rtype: datetime
        """
        return self._change_time

    @change_time.setter
    def change_time(self, change_time):
        """Sets the change_time of this Ip.

        Defines the date and time of the last object change.  # noqa: E501

        :param change_time: The change_time of this Ip.  # noqa: E501
        :type: datetime
        """

        self._change_time = change_time

    @property
    def ip(self):
        """Gets the ip of this Ip.  # noqa: E501

        Defines the IP Address (v4 or v6).  # noqa: E501

        :return: The ip of this Ip.  # noqa: E501
        :rtype: str
        """
        return self._ip

    @ip.setter
    def ip(self, ip):
        """Sets the ip of this Ip.

        Defines the IP Address (v4 or v6).  # noqa: E501

        :param ip: The ip of this Ip.  # noqa: E501
        :type: str
        """

        self._ip = ip

    @property
    def family(self):
        """Gets the family of this Ip.  # noqa: E501

        The IP Address family (v4 or v6).  # noqa: E501

        :return: The family of this Ip.  # noqa: E501
        :rtype: str
        """
        return self._family

    @family.setter
    def family(self, family):
        """Sets the family of this Ip.

        The IP Address family (v4 or v6).  # noqa: E501

        :param family: The family of this Ip.  # noqa: E501
        :type: str
        """
        allowed_values = ["4", "6"]  # noqa: E501
        if family not in allowed_values:
            raise ValueError(
                "Invalid value for `family` ({0}), must be one of {1}"  # noqa: E501
                .format(family, allowed_values)
            )

        self._family = family

    @property
    def location_iata(self):
        """Gets the location_iata of this Ip.  # noqa: E501

        Uses IATA airport code, which works as a location identifier.  # noqa: E501

        :return: The location_iata of this Ip.  # noqa: E501
        :rtype: str
        """
        return self._location_iata

    @location_iata.setter
    def location_iata(self, location_iata):
        """Sets the location_iata of this Ip.

        Uses IATA airport code, which works as a location identifier.  # noqa: E501

        :param location_iata: The location_iata of this Ip.  # noqa: E501
        :type: str
        """

        self._location_iata = location_iata

    @property
    def reverse_dns(self):
        """Gets the reverse_dns of this Ip.  # noqa: E501

        Defines the reverse DNS entry for the IP Address (PTR Resource Record).  # noqa: E501

        :return: The reverse_dns of this Ip.  # noqa: E501
        :rtype: str
        """
        return self._reverse_dns

    @reverse_dns.setter
    def reverse_dns(self, reverse_dns):
        """Sets the reverse_dns of this Ip.

        Defines the reverse DNS entry for the IP Address (PTR Resource Record).  # noqa: E501

        :param reverse_dns: The reverse_dns of this Ip.  # noqa: E501
        :type: str
        """

        self._reverse_dns = reverse_dns

    @property
    def current_price(self):
        """Gets the current_price of this Ip.  # noqa: E501

        Deprecated  # noqa: E501

        :return: The current_price of this Ip.  # noqa: E501
        :rtype: float
        """
        return self._current_price

    @current_price.setter
    def current_price(self, current_price):
        """Sets the current_price of this Ip.

        Deprecated  # noqa: E501

        :param current_price: The current_price of this Ip.  # noqa: E501
        :type: float
        """

        self._current_price = current_price

    @property
    def usage_in_minutes(self):
        """Gets the usage_in_minutes of this Ip.  # noqa: E501

        Total minutes the object has been running.  # noqa: E501

        :return: The usage_in_minutes of this Ip.  # noqa: E501
        :rtype: int
        """
        return self._usage_in_minutes

    @usage_in_minutes.setter
    def usage_in_minutes(self, usage_in_minutes):
        """Sets the usage_in_minutes of this Ip.

        Total minutes the object has been running.  # noqa: E501

        :param usage_in_minutes: The usage_in_minutes of this Ip.  # noqa: E501
        :type: int
        """

        self._usage_in_minutes = usage_in_minutes

    @property
    def name(self):
        """Gets the name of this Ip.  # noqa: E501

        The human-readable name of the object. It supports the full UTF-8 character set, with a maximum of 64 characters.  # noqa: E501

        :return: The name of this Ip.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Ip.

        The human-readable name of the object. It supports the full UTF-8 character set, with a maximum of 64 characters.  # noqa: E501

        :param name: The name of this Ip.  # noqa: E501
        :type: str
        """

        self._name = name

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
        if issubclass(Ip, dict):
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
        if not isinstance(other, Ip):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
