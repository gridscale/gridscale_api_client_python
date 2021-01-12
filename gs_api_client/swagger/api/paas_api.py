# coding: utf-8

"""
    API Specification

    # Introduction Welcome to gridscales API documentation.  A REST API is a programming interface that allows you to access and send data directly to our systems using HTTPS requests, without the need to use a web GUI. All the functionality you are already familiar with in your control panel is accessible through the API, including expert methods that are only available through the API. Allowing you to script any actions you require, regardless of their complexity.  First we will start with a general overview about how the API works, followed by an extensive list of each endpoint, describing them in great detail.  ## Requests  For security, gridscale requires all API requests are made through the HTTPS protocol so that traffic is encrypted. The following table displays the different type of requests that the interface responds to, depending on the action you require.  | Method | Description | | --- | --- | | GET | A simple search of information. The response is a JSON object. Requests using GET are always read-only. | | POST | Adds new objects and object relations. The POST request must contain all the required parameters in the form of a JSON object. | | PATCH | Changes an object or an object relation. The parameters in PATCH requests are usually optional, so only the changed parameters must be specified in a JSON object. | | DELETE | Deletes an object or object relation. The object is deleted if it exists. | | OPTIONS | Get an extensive list of the servers support methods and characteristics. We will not give example OPTION requests on each endpoint, as they are extensive and self-descriptive. |  <aside class=\"notice\"> The methods PATCH and DELETE are idempotent - that is, a request with identical parameters can be sent several times, and it doesn't change the result. </aside>  ## Status Codes  | HTTP Status | `Message` | Description | | --- | --- | --- | | 200 | `OK` | The request has been successfully processed and the result of the request is transmitted in the response. | | 202 | `Accepted` | The request has been accepted, but will run at a later date. Meaning we can not guarantee the success of the request. You should poll the request to be notified once the resource has been provisioned - see the requests endpoint on how to poll. | | 204 | `No Content` | The request was successful, but the answer deliberately contains no data. | | 400 | `Bad Request` | The request message was built incorrectly. | | 401 | `Unauthorised` | The request can not be performed without a valid authentication. X-Auth UserId or X-Auth token HTTP header is not set or the userID / token is invalid. | | 402 | `Payment Required` | Action can not be executed - not provided any or invalid payment methods. | | 403 | `Forbidden` | The request was not carried out due to lack of authorization of the user or because an impossible action was requested. | | 404 | `Not Found` | The requested resource was not found. Will also be used if you do a resource exists, but the user does not have permission for it. | | 405 | `Method Not Allowed` | The request may be made only with other HTTP methods (eg GET rather than POST). | | 409 | `Conflict` | The request was made under false assumptions. For example, a user can not be created twice with the same email. | | 415 | `Unsupported Media Type` | The contents of the request have been submitted with an invalid media type. All POST or PATCH requests must have \"Content-Type : application / json\" as a header, and send a JSON object as a payload. | | 416 | `Requested Range Not Satisfiable` | The request could not be fulfilled. It is possible that a resource limit was reached or an IPv4 address pool is exhausted. | | 424 | `Failed Dependency` | The request could not be performed because the object is in the wrong status. | | 429 | `Too Many Requests` | The request has been rejected because rate limits have been exceeded. |  <aside class=\"success\"> Status 200-204 indicates that the request has been accepted and is processed. </aside> <aside class=\"notice\"> Status 400-429 indicates that there was a problem with the request that originated on the client. You will find more information about the problem in the body of 4xx response. </aside> <aside class=\"warning\"> A status 500 means that there was a server-side problem and your request can not be processed now. </aside>  ## Request Headers  | Header | Description | | --- | --- | | Content-Type | Always \"application/json\". | | X-Auth-userId | The user UUID. This can be found in the panel under \"API\" and will never change ( even after the change of user e-mail). | | X-Auth-Token | Is generated from the API hash and must be sent with all API requests. Both the token and its permissions can be configured in the panel.|  ## Response Headers  | Header | Description | | --- | --- | | Content-Type | Always \"application/json\". | | X-Time-Provisioning | The time taken to process the request (in ms). | | X-Api-Identity | The currently active Provisioning API version. Useful when reporting bugs to us. | | X-Request-Id   | The unique identifier of the request, be sure to include it when referring to a request. | | RateLimit-Limit | The number of requests that can be made per minute. | | RateLimit-Remaining | The number of requests that still remain before you hit your request limit. | | RateLimit-Reset | A [Unix timestamp](https://en.wikipedia.org/wiki/Unix_time) in milliseconds of when the rate limit will reset, or the time at which a request no longer will return 429 - Too Many Requests. |  ## Timestamp Format  All timestamps follow <a href=\"https://de.wikipedia.org/wiki/ISO_8601\" target=\"_blank_\">ISO 8601</a> and issued in <a href=\"https://www.timeanddate.de/zeitzonen/utc-gmt\" target=\"_blank_\">UTC</a>  ## CORS  ### Cross Origin Resource Sharing  To allow API access from other domains that supports the API CORS (Cross Origin Resource Sharing). See: enable-cors.org/ .  This allows direct use the API in the browser running a JavaScript web control panel.  All this is done in the background by the browser. The following HTTP headers are set by the API:  Header | Parameter | Description --- | --- | --- Access-Control-Allow-Methods   | GET, POST, PUT, PATCH, DELETE, OPTIONS | Contains all available methods that may be used for queries. Access-Control-Allow-Credentials | true | Is set to \"true\". Allows the browser to send the authentication data via X-Auth HTTP header. Access-Control-Allow-Headers | Origin, X-Requested-With, Content-Type, Accept, X-Auth-UserId, X-Auth-Token, X-Exec-Time, X-API-Version, X-Api-Client | The HTTP headers available for requests. Access-Control-Allow-Origin | * | The domain sent by the browser as a source of demand. Access-Control-Expose-Headers | X-Exec-Time, X-Api-Version | The HTTP headers that can be used by a browser application.  ## Rate Limits  The number of requests that can be made through our API is currently limited to 210 requests per 60 seconds. The current state of rate limiting is returned within the response headers of each request. The relevant response headers are  - RateLimit-Limit - RateLimit-Remaining - RateLimit-Reset  See the Response Headers section for details.  As long as the `RateLimit-Remaining` count is above zero, you will be able to make further requests. As soon as the `RateLimit-Remaining` header value is zero, subsequent requests will return the 429 status code. This will stay until the timestamp given in `RateLimit-Reset` has been reached.  ### Example rate limiting response  ```shell HTTP/1.0 429 TOO MANY REQUESTS Content-Length: 66 Content-Type: application/json; charset=utf-8 Date: Mon, 11 Nov 2019 11:11:33 GMT RateLimit-Limit: 210 RateLimit-Remaining: 0 RateLimit-Reset: 1573468299256  {     \"id\": \"too_many_requests\",     \"message\": \"API Rate limit exceeded.\" } ```  It is important to understand how rate limits are reset in order to use the API efficiently. Rate limits are reset for all counted requests at once. This means that that once the timestamp `RateLimit-Remaining` has arrived all counted request are reset and you can again start sending requests to the API.  This allows for short burst of traffic. The downside is once you have hit the request limit no more requests are allowed until the rate limit duration is reset.  ## Object Relations Relationships describe resource objects (storages, networks, IPs, etc.) that are connected to a server. These relationships are treated like objects themselves and can have properties specific to this relation.  One example would be, that the MAC address of a private network connected to a server (Server-to-Network relation) can be found as property of the relation itself - the relation is the _network interface_ in the server.  Another example is storage, where the SCSI LUN is also part of the Server-to-Storage relation object.  This information is especially interesting if some kind of network boot is used on the servers, where the properties of the server need to be known beforehand.  ## Deleted Objects Objects that are deleted are no longer visible on their *regular* endpoints. For historical reasons these objects are still available read-only on a special endpoint named /deleted. If objects have been deleted but have not yet been billed in the current period, the yet-to-be-billed price is still shown.  <!-- #strip_js --> ## Node.js Library  We have a JavaScript library for you to use our API with ease.  <a href=\"https://www.npmjs.com/package/@gridscale/api\" target=\"_blank\"><img src=\"https://badge.fury.io/js/%40gridscale%2Fapi.svg\" alt=\"npm badge\"></a>  <aside class=\"success\"> We want to make it even easier for you to manage your Infrastructure via our API - so feel free to contact us with any ideas, or languages you would like to see included. </aside>  Requests with our Node.js lib return a little differently. Everything is the same except it allows you to add URL parameters to customize your requests.  To get started <a href=\"https://www.npmjs.com/package/@gridscale/api\" target=\"_blank\">click here</a> .  <!-- #strip_js_end -->  <!-- #strip_go --> ## Golang Library We also have a Golang library for Gophers.  Requests with our Golang lib return a little differently. Everything is the same except it allows you to add URL parameters to customize your requests.  To get started <a href=\"https://github.com/gridscale/gsclient-go\" target=\"_blank\">click here</a> .  <!-- #strip_go_end -->  <!-- #strip_python --> ## Python Library  We have a Python library, that optionally also simplifies handling of asynchronous requests by mimicking synchronous blocking behaviour.  To get started <a href=\"https://pypi.org/project/gs-api-client/\" target=\"_blank\">click here</a> .  <!-- #strip_python_end -->  # Authentication  In order to use the API, the User-UUID and an API_Token are required. Both are available via the web GUI which can be found here on <a href=\"https://my.gridscale.io/APIs/\" target=\"_blank\">Your Account</a>  <aside class=\"success\"> If you are logged in, your UUID and Token will be pulled dynamically from your account, so you can copy request examples straight into your code. </aside>  The User-UUID remains the same, even if the users email address is changed. The API_Token is a randomly generated hash that allows read/write access.  ## API_Token  <table class=\"security-details\"><tbody><tr><th> Security scheme type: </th><td> API Key </td></tr><tr><th> header parameter name:</th><td> X-Auth-Token </td></tr></tbody></table>  ## User_UUID  <table class=\"security-details\"><tbody><tr><th> Security scheme type: </th><td> API Key </td></tr><tr><th> header parameter name:</th><td> X-Auth-UserId </td></tr></tbody></table>  ## Examples  <!-- #strip_js --> > Node.js ``` // to get started // read the docs @ https://www.npmjs.com/package/@gs_js_auth/api var gs_js_auth = require('@gs_js_auth/api').gs_js_auth; var client = new gs_js_auth.Client(\"##API_TOKEN##\",\"##USER_UUID##\"); ``` <!-- #strip_js_end -->  <!-- #strip_go --> > Golang ``` // to get started // read the docs @ https://github.com/gridscale/gsclient-go config := gsclient.NewConfiguration(   \"https://api.gridscale.io\",   \"##USER_UUID##\",   \"##API_TOKEN##\",   false, //set debug mode ) client := gsclient.NewClient(config) ``` <!-- #strip_go_end -->  > Shell Authentication Headers ```   -H \"X-Auth-UserId: ##USER_UUID##\" \\   -H \"X-Auth-Token: ##API_TOKEN##\" \\ ```  > Setting Authentication in your Environment variables ``` export API_TOKEN=\"##API_TOKEN##\" USER_UUID=\"##USER_UUID##\" ```  <aside class=\"notice\"> You must replace <code>USER_UUID</code> and <code>API_Token</code> with your personal UUID and API key respectively. </aside>   # noqa: E501

    OpenAPI spec version: 1.0.24
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from gs_api_client.swagger.api_client import ApiClient


class PaasApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_paas_security_zone(self, body, **kwargs):  # noqa: E501
        """Security Zones Post  # noqa: E501

        https://api.gridscale.io/objects/paas/security_zones To create a new security zone.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_paas_security_zone(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param PaasSecurityZoneCreate body: Data for a new security_zones (required)
        :return: PaasSecurityZoneCreateResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_paas_security_zone_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_paas_security_zone_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def create_paas_security_zone_with_http_info(self, body, **kwargs):  # noqa: E501
        """Security Zones Post  # noqa: E501

        https://api.gridscale.io/objects/paas/security_zones To create a new security zone.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_paas_security_zone_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param PaasSecurityZoneCreate body: Data for a new security_zones (required)
        :return: PaasSecurityZoneCreateResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_paas_security_zone" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_paas_security_zone`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['API_Token', 'User_UUID']  # noqa: E501

        return self.api_client.call_api(
            '/objects/paas/security_zones', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PaasSecurityZoneCreateResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_paas_service(self, payload, **kwargs):  # noqa: E501
        """PaaS Post  # noqa: E501

        https://api.gridscale.io/objects/paas/services To create a new PaaS service.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_paas_service(payload, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param PaasServiceCreate payload: Data for a new PaaS task (required)
        :return: PaasServiceCreateResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_paas_service_with_http_info(payload, **kwargs)  # noqa: E501
        else:
            (data) = self.create_paas_service_with_http_info(payload, **kwargs)  # noqa: E501
            return data

    def create_paas_service_with_http_info(self, payload, **kwargs):  # noqa: E501
        """PaaS Post  # noqa: E501

        https://api.gridscale.io/objects/paas/services To create a new PaaS service.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_paas_service_with_http_info(payload, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param PaasServiceCreate payload: Data for a new PaaS task (required)
        :return: PaasServiceCreateResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['payload']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_paas_service" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'payload' is set
        if ('payload' not in params or
                params['payload'] is None):
            raise ValueError("Missing the required parameter `payload` when calling `create_paas_service`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'payload' in params:
            body_params = params['payload']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['API_Token', 'User_UUID']  # noqa: E501

        return self.api_client.call_api(
            '/objects/paas/services', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PaasServiceCreateResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_paas_service(self, paas_service_uuid, **kwargs):  # noqa: E501
        """PaaS Delete  # noqa: E501

        https://api.gridscale.io/objects/paas/services/{paas_service_uuid} To delete the specified PaaS service.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_paas_service(paas_service_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str paas_service_uuid: object that need to be deleted (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_paas_service_with_http_info(paas_service_uuid, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_paas_service_with_http_info(paas_service_uuid, **kwargs)  # noqa: E501
            return data

    def delete_paas_service_with_http_info(self, paas_service_uuid, **kwargs):  # noqa: E501
        """PaaS Delete  # noqa: E501

        https://api.gridscale.io/objects/paas/services/{paas_service_uuid} To delete the specified PaaS service.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_paas_service_with_http_info(paas_service_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str paas_service_uuid: object that need to be deleted (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['paas_service_uuid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_paas_service" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'paas_service_uuid' is set
        if ('paas_service_uuid' not in params or
                params['paas_service_uuid'] is None):
            raise ValueError("Missing the required parameter `paas_service_uuid` when calling `delete_paas_service`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'paas_service_uuid' in params:
            path_params['paas_service_uuid'] = params['paas_service_uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['API_Token', 'User_UUID']  # noqa: E501

        return self.api_client.call_api(
            '/objects/paas/services/{paas_service_uuid}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_paas_service(self, paas_service_uuid, **kwargs):  # noqa: E501
        """PaaS Get  # noqa: E501

        https://api.gridscale.io/objects/paas/services/{paas_service_uuid} To retrieve detailed information about the specified PaaS service.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_paas_service(paas_service_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str paas_service_uuid: ID of paas (required)
        :return: PaasServiceGetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_paas_service_with_http_info(paas_service_uuid, **kwargs)  # noqa: E501
        else:
            (data) = self.get_paas_service_with_http_info(paas_service_uuid, **kwargs)  # noqa: E501
            return data

    def get_paas_service_with_http_info(self, paas_service_uuid, **kwargs):  # noqa: E501
        """PaaS Get  # noqa: E501

        https://api.gridscale.io/objects/paas/services/{paas_service_uuid} To retrieve detailed information about the specified PaaS service.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_paas_service_with_http_info(paas_service_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str paas_service_uuid: ID of paas (required)
        :return: PaasServiceGetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['paas_service_uuid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_paas_service" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'paas_service_uuid' is set
        if ('paas_service_uuid' not in params or
                params['paas_service_uuid'] is None):
            raise ValueError("Missing the required parameter `paas_service_uuid` when calling `get_paas_service`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'paas_service_uuid' in params:
            path_params['paas_service_uuid'] = params['paas_service_uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['API_Token', 'User_UUID']  # noqa: E501

        return self.api_client.call_api(
            '/objects/paas/services/{paas_service_uuid}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PaasServiceGetResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_paas_service_metrics(self, paas_service_uuid, **kwargs):  # noqa: E501
        """PaaS Metrics  # noqa: E501

        https://api.gridscale.io/objects/paas/services/{paas_service_uuid}/metrics To retrieve information about usage metrics of the specified PaaS service.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_paas_service_metrics(paas_service_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str paas_service_uuid: service for which to return metrics (required)
        :return: PaasServiceMetricsGetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_paas_service_metrics_with_http_info(paas_service_uuid, **kwargs)  # noqa: E501
        else:
            (data) = self.get_paas_service_metrics_with_http_info(paas_service_uuid, **kwargs)  # noqa: E501
            return data

    def get_paas_service_metrics_with_http_info(self, paas_service_uuid, **kwargs):  # noqa: E501
        """PaaS Metrics  # noqa: E501

        https://api.gridscale.io/objects/paas/services/{paas_service_uuid}/metrics To retrieve information about usage metrics of the specified PaaS service.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_paas_service_metrics_with_http_info(paas_service_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str paas_service_uuid: service for which to return metrics (required)
        :return: PaasServiceMetricsGetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['paas_service_uuid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_paas_service_metrics" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'paas_service_uuid' is set
        if ('paas_service_uuid' not in params or
                params['paas_service_uuid'] is None):
            raise ValueError("Missing the required parameter `paas_service_uuid` when calling `get_paas_service_metrics`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'paas_service_uuid' in params:
            path_params['paas_service_uuid'] = params['paas_service_uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['API_Token', 'User_UUID']  # noqa: E501

        return self.api_client.call_api(
            '/objects/paas/services/{paas_service_uuid}/metrics', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PaasServiceMetricsGetResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_paas_service_templates(self, **kwargs):  # noqa: E501
        """PaaS Service Templates Get  # noqa: E501

        https://api.gridscale.io/objects/paas/service_templates To retrieve detailed information about all PaaS service templates.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_paas_service_templates(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: PaasServiceTemplatesGetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_paas_service_templates_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_paas_service_templates_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_paas_service_templates_with_http_info(self, **kwargs):  # noqa: E501
        """PaaS Service Templates Get  # noqa: E501

        https://api.gridscale.io/objects/paas/service_templates To retrieve detailed information about all PaaS service templates.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_paas_service_templates_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: PaasServiceTemplatesGetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_paas_service_templates" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['API_Token', 'User_UUID']  # noqa: E501

        return self.api_client.call_api(
            '/objects/paas/service_templates', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PaasServiceTemplatesGetResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_paas_services(self, **kwargs):  # noqa: E501
        """PaaS Get  # noqa: E501

        https://api.gridscale.io/objects/paas/services To retrieve detailed information about all PaaS services.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_paas_services(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: PaasServicesGetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_paas_services_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_paas_services_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_paas_services_with_http_info(self, **kwargs):  # noqa: E501
        """PaaS Get  # noqa: E501

        https://api.gridscale.io/objects/paas/services To retrieve detailed information about all PaaS services.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_paas_services_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: PaasServicesGetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_paas_services" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['API_Token', 'User_UUID']  # noqa: E501

        return self.api_client.call_api(
            '/objects/paas/services', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PaasServicesGetResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def renew_paas_service_credentials(self, paas_service_uuid, payload, **kwargs):  # noqa: E501
        """Renew PaaS credentials  # noqa: E501

        https://api.gridscale.io/objects/paas/services/{paas_service_uuid}/renew_credentials To renew credentials for gridscale Kubernetes PaaS service templates.  The credentials of a PaaS service will be renewed (if supported by service template). Updated credentials can be found in attribute `credentials` of service, once request processing has finished.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.renew_paas_service_credentials(paas_service_uuid, payload, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str paas_service_uuid: object that need to be updated. (required)
        :param object payload: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.renew_paas_service_credentials_with_http_info(paas_service_uuid, payload, **kwargs)  # noqa: E501
        else:
            (data) = self.renew_paas_service_credentials_with_http_info(paas_service_uuid, payload, **kwargs)  # noqa: E501
            return data

    def renew_paas_service_credentials_with_http_info(self, paas_service_uuid, payload, **kwargs):  # noqa: E501
        """Renew PaaS credentials  # noqa: E501

        https://api.gridscale.io/objects/paas/services/{paas_service_uuid}/renew_credentials To renew credentials for gridscale Kubernetes PaaS service templates.  The credentials of a PaaS service will be renewed (if supported by service template). Updated credentials can be found in attribute `credentials` of service, once request processing has finished.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.renew_paas_service_credentials_with_http_info(paas_service_uuid, payload, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str paas_service_uuid: object that need to be updated. (required)
        :param object payload: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['paas_service_uuid', 'payload']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method renew_paas_service_credentials" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'paas_service_uuid' is set
        if ('paas_service_uuid' not in params or
                params['paas_service_uuid'] is None):
            raise ValueError("Missing the required parameter `paas_service_uuid` when calling `renew_paas_service_credentials`")  # noqa: E501
        # verify the required parameter 'payload' is set
        if ('payload' not in params or
                params['payload'] is None):
            raise ValueError("Missing the required parameter `payload` when calling `renew_paas_service_credentials`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'paas_service_uuid' in params:
            path_params['paas_service_uuid'] = params['paas_service_uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'payload' in params:
            body_params = params['payload']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['API_Token', 'User_UUID']  # noqa: E501

        return self.api_client.call_api(
            '/objects/paas/services/{paas_service_uuid}/renew_credentials', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_paas_service(self, paas_service_uuid, payload, **kwargs):  # noqa: E501
        """PaaS Patch  # noqa: E501

        https://api.gridscale.io/objects/paas/services/{paas_service_uuid} To update the attributes of the specified PaaS service.  If resource_limits is omitted, it will be left unchanged. If resource_limits is an empty list, all limits will be unset. If parameters is omitted, it will be left unchanged. If parameters is an empty object, all parameters will be unset. **Attention**: If parameters are changed while a service is running, the service will be restarted and you may experience some downtime.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_paas_service(paas_service_uuid, payload, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str paas_service_uuid: object that need to be updated. (required)
        :param PaasServiceUpdate payload: Updated PaaS (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_paas_service_with_http_info(paas_service_uuid, payload, **kwargs)  # noqa: E501
        else:
            (data) = self.update_paas_service_with_http_info(paas_service_uuid, payload, **kwargs)  # noqa: E501
            return data

    def update_paas_service_with_http_info(self, paas_service_uuid, payload, **kwargs):  # noqa: E501
        """PaaS Patch  # noqa: E501

        https://api.gridscale.io/objects/paas/services/{paas_service_uuid} To update the attributes of the specified PaaS service.  If resource_limits is omitted, it will be left unchanged. If resource_limits is an empty list, all limits will be unset. If parameters is omitted, it will be left unchanged. If parameters is an empty object, all parameters will be unset. **Attention**: If parameters are changed while a service is running, the service will be restarted and you may experience some downtime.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_paas_service_with_http_info(paas_service_uuid, payload, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str paas_service_uuid: object that need to be updated. (required)
        :param PaasServiceUpdate payload: Updated PaaS (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['paas_service_uuid', 'payload']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_paas_service" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'paas_service_uuid' is set
        if ('paas_service_uuid' not in params or
                params['paas_service_uuid'] is None):
            raise ValueError("Missing the required parameter `paas_service_uuid` when calling `update_paas_service`")  # noqa: E501
        # verify the required parameter 'payload' is set
        if ('payload' not in params or
                params['payload'] is None):
            raise ValueError("Missing the required parameter `payload` when calling `update_paas_service`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'paas_service_uuid' in params:
            path_params['paas_service_uuid'] = params['paas_service_uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'payload' in params:
            body_params = params['payload']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['API_Token', 'User_UUID']  # noqa: E501

        return self.api_client.call_api(
            '/objects/paas/services/{paas_service_uuid}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
