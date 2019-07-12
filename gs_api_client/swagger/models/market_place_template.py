# coding: utf-8

"""
    API Specification

    # Introduction Welcome to gridscales API documentation.  A REST API is a programming interface that allows you to access and send data directly to our systems using HTTPS requests, without the need to use a web GUI. All the functionality you are already familiar with in your control panel is accessible through the API, including expert methods that are only available through the API. Allowing you to script any actions you require, regardless of their complexity.  First we will start with a general overview about how the API works, followed by an extensive list of each endpoint, describing them in great detail.  ## Requests  For security, gridscale requires all API requests are made through the HTTPS protocol so that traffic is encrypted. The following table displays the different type of requests that the interface responds to, depending on the action you require.  | Method | Description | | --- | --- | | GET | A simple search of information. The response is a JSON object. Requests using GET are always read-only. | | POST | Adds new objects and object relations. The POST request must contain all the required parameters in the form of a JSON object. | | PATCH | Changes an object or an object relation. The parameters in PATCH requests are usually optional, so only the changed parameters must be specified in a JSON object. | | DELETE | Deletes an object or object relation. The object is deleted if it exists. | | OPTIONS | Get an extensive list of the servers support methods and characteristics. We will not give example OPTION requests on each endpoint, as they are extensive and self-descriptive. |  <aside class=\"notice\"> The methods PATCH and DELETE are idempotent - that is, a request with identical parameters can be sent several times, and it doesn't change the result. </aside>  ## Status Codes  | HTTP Status | `Message` | Description | | --- | --- | --- | | 200 | `OK` | The request has been successfully processed and the result of the request is transmitted in the response. | | 202 | `Accepted` | The request has been accepted, but will run at a later date. Meaning we can not guarantee the success of the request. You should poll the request to be notified once the resource has been provisioned - see the requests endpoint on how to poll. | | 204 | `No Content` | The request was successful, but the answer deliberately contains no data. | | 400 | `Bad Request` | The request message was built incorrectly. | | 401 | `Unauthorised` | The request can not be performed without a valid authentication. X-Auth UserId or X-Auth token HTTP header is not set or the userID / token is invalid. | | 402 | `Payment Required` | Action can not be executed - not provided any or invalid payment methods. | | 403 | `Forbidden` | The request was not carried out due to lack of authorization of the user or because an impossible action was requested. | | 404 | `Not Found` | The requested resource was not found. Will also be used if you do a resource exists, but the user does not have permission for it. | | 405 | `Method Not Allowed` | The request may be made only with other HTTP methods (eg GET rather than POST). | | 409 | `Conflict` | The request was made under false assumptions. For example, a user can not be created twice with the same email. | | 415 | `Unsupported Media Type` | The contents of the request have been submitted with an invalid media type. All POST or PATCH requests must have \"Content-Type : application / json\" as a header, and send a JSON object as a payload. | | 424 | `Failed Dependency` | The request could not be performed because the object is in the wrong status. |  <aside class=\"success\"> Status 200-204 indicates that the request has been accepted and is processed. </aside> <aside class=\"notice\"> Status 400-424 indicates that there was a problem with the request. For more information about the problem you'll find in the body of 4xx response. </aside> <aside class=\"warning\"> A status 500 means that there was a server-side problem and your request can not be processed now. </aside>  ## Request Headers  | Header | Description | | --- | --- | | Content-Type | Always \"applicaton/json\". | | X-Auth-userId | The user UUID. This can be found in the panel under \"API\" and will never change ( even after the change of user e-mail). | | X-Auth-Token | Is generated from the API hash and must be sent with all API requests. Both the token and its permissions can be configured in the panel.|  ## Response Headers  | Header | Description | | --- | --- | | Content-Type | Always \"application/json\". | | X-Exec-Time | The time taken to process the request (in ms). | | X-Api-Version | The currently active Provisioning API version. Useful when reporting bugs to us. |  ## Timestamp Format  All timestamps follow <a href=\"https://de.wikipedia.org/wiki/ISO_8601\" target=\"_blank_\">ISO 8601</a> and issued in <a href=\"https://www.timeanddate.de/zeitzonen/utc-gmt\" target=\"_blank_\">UTC</a>  ## CORS  ### Cross Origin Resource Sharing  To allow API access from other domains that supports the API CORS (Cross Origin Resource Sharing). See: enable-cors.org/ .  This allows direct use the API in the browser running a JavaScript web control panel.  All this is done in the background by the browser. The following HTTP headers are set by the API:  Header | Parameter | Description --- | --- | --- Access-Control-Allow-Methods   | GET, POST, PUT, PATCH, DELETE, OPTIONS | Contains all available methods that may be used for queries. Access-Control-Allow-Credentials | true | Is set to \"true\". Allows the browser to send the authentication data via X-Auth HTTP header. Access-Control-Allow-Headers | Origin, X-Requested-With, Content-Type, Accept, X-Auth-UserId, X-Auth-Token, X-Exec-Time, X-API-Version, X-Api-Client | The HTTP headers available for requests. Access-Control-Allow-Origin | * | The domain sent by the browser as a source of demand. Access-Control-Expose-Headers | X-Exec-Time, X-Api-Version | The HTTP headers that can be used by a browser application.  ## Object Relations Relationships describe resource objects (storages, networks, IPs, etc.) that are connected to a server. These relationships are treated like objects themselves and can have properties specific to this relation.  One example would be, that the MAC address of a private network connected to a server (Server-to-Network relation) can be found as property of the relation itself - the relation is the _network interface_ in the server.  Another example is storage, where the SCSI LUN is also part of the Server-to-Storage relation object.  This information is especially interesting if some kind of network boot is used on the servers, where the properties of the server need to be known beforehand.  ## Deleted Objects Objects that are deleted are no longer visible on their *regular* endpoints. For historical reasons these objects are still available read-only on a special endpoint named /deleted. If objects have been deleted but have not yet been billed in the current period, the yet-to-be-billed price is still shown.  <!-- #strip_js --> ## NodeJs Library  We have a JavaScript library for you to use our API with ease.  <a href=\"https://www.npmjs.com/package/@gridscale/api\" target=\"_blank\"><img src=\"https://badge.fury.io/js/%40gridscale%2Fapi.svg\" alt=\"npm badge\"></a>  <aside class=\"success\"> We want to make it even easier for you to manage your Infrastructure via our API - so feel free to contact us with any ideas, or languages you would like to see included. </aside>  Requests with our NodeJs lib return a little differently. Everything is the same except it allows you to add URL parameters to customize your requests.  To get started <a href=\"https://www.npmjs.com/package/@gridscale/api\" target=\"_blank\">click here</a> .  <!-- #strip_js_end -->  # Authentication  In order to use the API, the User-UUID and an API_Token are required. Both are available via the web GUI which can be found here on <a href=\"https://my.gridscale.io/APIs/\" target=\"_blank\">Your Account</a>  <aside class=\"success\"> If your are logged in, your UUID and Token will be pulled dynamically from your account, so you can copy request examples straight into your code. </aside>  The User-UUID remains the same, even if the users email address is changed. The API_Token is a randomly generated hash that allows read/write access.  ## API_Token  <table class=\"security-details\"><tbody><tr><th> Security scheme type: </th><td> API Key </td></tr><tr><th> header parameter name:</th><td> X-Auth-Token </td></tr></tbody></table>  ## User_UUID  <table class=\"security-details\"><tbody><tr><th> Security scheme type: </th><td> API Key </td></tr><tr><th> header parameter name:</th><td> X-Auth-UserId </td></tr></tbody></table>  ## Examples  <!-- #strip_js --> > NodeJS ``` // to get started // read the docs @ https://www.npmjs.com/package/@gs_js_auth/api var gs_js_auth = require('@gs_js_auth/api').gs_js_auth; var client = new gs_js_auth.Client(\"##API_TOKEN##\",\"##USER_UUID##\"); ``` <!-- #strip_js_end -->  > Shell Authentication Headers ```   -H \"X-Auth-UserId: ##USER_UUID##\" \\   -H \"X-Auth-Token: ##API_TOKEN##\" \\ ```  > Setting Authentication in your Environment variables ``` export API_TOKEN=\"##API_TOKEN##\" USER_UUID=\"##USER_UUID##\" ```  <aside class=\"notice\"> You must replace <code>USER_UUID</code> and <code>API_Token</code> with your personal UUID and API key respectively. </aside>   # noqa: E501

    OpenAPI spec version: 1.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MarketPlaceTemplate(object):
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
        'capacity': 'int',
        'change_time': 'datetime',
        'create_time': 'datetime',
        'labels': 'list[str]',
        'name': 'str',
        'object_storage_path': 'str',
        'object_uuid': 'str',
        'status': 'str',
        'template_type': 'str',
        'unique_hash': 'str'
    }

    attribute_map = {
        'capacity': 'capacity',
        'change_time': 'change_time',
        'create_time': 'create_time',
        'labels': 'labels',
        'name': 'name',
        'object_storage_path': 'object_storage_path',
        'object_uuid': 'object_uuid',
        'status': 'status',
        'template_type': 'template_type',
        'unique_hash': 'unique_hash'
    }

    def __init__(self, capacity=None, change_time=None, create_time=None, labels=None, name=None, object_storage_path=None, object_uuid=None, status=None, template_type=None, unique_hash=None):  # noqa: E501
        """MarketPlaceTemplate - a model defined in Swagger"""  # noqa: E501

        self._capacity = None
        self._change_time = None
        self._create_time = None
        self._labels = None
        self._name = None
        self._object_storage_path = None
        self._object_uuid = None
        self._status = None
        self._template_type = None
        self._unique_hash = None
        self.discriminator = None

        if capacity is not None:
            self.capacity = capacity
        if change_time is not None:
            self.change_time = change_time
        if create_time is not None:
            self.create_time = create_time
        if labels is not None:
            self.labels = labels
        if name is not None:
            self.name = name
        if object_storage_path is not None:
            self.object_storage_path = object_storage_path
        if object_uuid is not None:
            self.object_uuid = object_uuid
        if status is not None:
            self.status = status
        if template_type is not None:
            self.template_type = template_type
        if unique_hash is not None:
            self.unique_hash = unique_hash

    @property
    def capacity(self):
        """Gets the capacity of this MarketPlaceTemplate.  # noqa: E501

        The capacity of a storage/ISO-Image/template/snapshot in GB.  # noqa: E501

        :return: The capacity of this MarketPlaceTemplate.  # noqa: E501
        :rtype: int
        """
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        """Sets the capacity of this MarketPlaceTemplate.

        The capacity of a storage/ISO-Image/template/snapshot in GB.  # noqa: E501

        :param capacity: The capacity of this MarketPlaceTemplate.  # noqa: E501
        :type: int
        """

        self._capacity = capacity

    @property
    def change_time(self):
        """Gets the change_time of this MarketPlaceTemplate.  # noqa: E501

        Defines the date and time of the last object change.  # noqa: E501

        :return: The change_time of this MarketPlaceTemplate.  # noqa: E501
        :rtype: datetime
        """
        return self._change_time

    @change_time.setter
    def change_time(self, change_time):
        """Sets the change_time of this MarketPlaceTemplate.

        Defines the date and time of the last object change.  # noqa: E501

        :param change_time: The change_time of this MarketPlaceTemplate.  # noqa: E501
        :type: datetime
        """

        self._change_time = change_time

    @property
    def create_time(self):
        """Gets the create_time of this MarketPlaceTemplate.  # noqa: E501

        Defines the date and time the object was initially created.  # noqa: E501

        :return: The create_time of this MarketPlaceTemplate.  # noqa: E501
        :rtype: datetime
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this MarketPlaceTemplate.

        Defines the date and time the object was initially created.  # noqa: E501

        :param create_time: The create_time of this MarketPlaceTemplate.  # noqa: E501
        :type: datetime
        """

        self._create_time = create_time

    @property
    def labels(self):
        """Gets the labels of this MarketPlaceTemplate.  # noqa: E501

        List of labels.  # noqa: E501

        :return: The labels of this MarketPlaceTemplate.  # noqa: E501
        :rtype: list[str]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this MarketPlaceTemplate.

        List of labels.  # noqa: E501

        :param labels: The labels of this MarketPlaceTemplate.  # noqa: E501
        :type: list[str]
        """

        self._labels = labels

    @property
    def name(self):
        """Gets the name of this MarketPlaceTemplate.  # noqa: E501

        The human-readable name of the object. It supports the full UTF-8 charset, with a maximum of 64 characters.  # noqa: E501

        :return: The name of this MarketPlaceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MarketPlaceTemplate.

        The human-readable name of the object. It supports the full UTF-8 charset, with a maximum of 64 characters.  # noqa: E501

        :param name: The name of this MarketPlaceTemplate.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def object_storage_path(self):
        """Gets the object_storage_path of this MarketPlaceTemplate.  # noqa: E501

        s3//  # noqa: E501

        :return: The object_storage_path of this MarketPlaceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._object_storage_path

    @object_storage_path.setter
    def object_storage_path(self, object_storage_path):
        """Sets the object_storage_path of this MarketPlaceTemplate.

        s3//  # noqa: E501

        :param object_storage_path: The object_storage_path of this MarketPlaceTemplate.  # noqa: E501
        :type: str
        """

        self._object_storage_path = object_storage_path

    @property
    def object_uuid(self):
        """Gets the object_uuid of this MarketPlaceTemplate.  # noqa: E501

        The UUID of an object is always unique, and refers to a specific object.  # noqa: E501

        :return: The object_uuid of this MarketPlaceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._object_uuid

    @object_uuid.setter
    def object_uuid(self, object_uuid):
        """Sets the object_uuid of this MarketPlaceTemplate.

        The UUID of an object is always unique, and refers to a specific object.  # noqa: E501

        :param object_uuid: The object_uuid of this MarketPlaceTemplate.  # noqa: E501
        :type: str
        """

        self._object_uuid = object_uuid

    @property
    def status(self):
        """Gets the status of this MarketPlaceTemplate.  # noqa: E501

        Status indicates the status of the object.  # noqa: E501

        :return: The status of this MarketPlaceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this MarketPlaceTemplate.

        Status indicates the status of the object.  # noqa: E501

        :param status: The status of this MarketPlaceTemplate.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def template_type(self):
        """Gets the template_type of this MarketPlaceTemplate.  # noqa: E501

        the type of template  # noqa: E501

        :return: The template_type of this MarketPlaceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._template_type

    @template_type.setter
    def template_type(self, template_type):
        """Sets the template_type of this MarketPlaceTemplate.

        the type of template  # noqa: E501

        :param template_type: The template_type of this MarketPlaceTemplate.  # noqa: E501
        :type: str
        """

        self._template_type = template_type

    @property
    def unique_hash(self):
        """Gets the unique_hash of this MarketPlaceTemplate.  # noqa: E501

        unique hash to allow user to import the self-created marketplace template  # noqa: E501

        :return: The unique_hash of this MarketPlaceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._unique_hash

    @unique_hash.setter
    def unique_hash(self, unique_hash):
        """Sets the unique_hash of this MarketPlaceTemplate.

        unique hash to allow user to import the self-created marketplace template  # noqa: E501

        :param unique_hash: The unique_hash of this MarketPlaceTemplate.  # noqa: E501
        :type: str
        """

        self._unique_hash = unique_hash

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
        if issubclass(MarketPlaceTemplate, dict):
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
        if not isinstance(other, MarketPlaceTemplate):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
