# coding: utf-8

"""
    Contabo API


    OpenAPI spec version: 1.0.0
    Contact: support@contabo.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from pfruck_contabo.api_client import ApiClient


class InternalApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_object_storage_credentials(self, x_request_id, user_id, **kwargs):  # noqa: E501
        """Get S3 compatible object storage credentials  # noqa: E501

        Get S3 compatible object storage credentials for accessing it via S3 compatible tools like `aws` cli.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_object_storage_credentials(x_request_id, user_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_request_id: [Uuid4](https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)) to identify individual requests for support cases. You can use [uuidgenerator](https://www.uuidgenerator.net/version4) to generate them manually. (required)
        :param str user_id: The identifier of the user (required)
        :param str x_trace_id: Identifier to trace group of requests.
        :return: CredentialResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_object_storage_credentials_with_http_info(x_request_id, user_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_object_storage_credentials_with_http_info(x_request_id, user_id, **kwargs)  # noqa: E501
            return data

    def get_object_storage_credentials_with_http_info(self, x_request_id, user_id, **kwargs):  # noqa: E501
        """Get S3 compatible object storage credentials  # noqa: E501

        Get S3 compatible object storage credentials for accessing it via S3 compatible tools like `aws` cli.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_object_storage_credentials_with_http_info(x_request_id, user_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_request_id: [Uuid4](https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)) to identify individual requests for support cases. You can use [uuidgenerator](https://www.uuidgenerator.net/version4) to generate them manually. (required)
        :param str user_id: The identifier of the user (required)
        :param str x_trace_id: Identifier to trace group of requests.
        :return: CredentialResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_request_id', 'user_id', 'x_trace_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_object_storage_credentials" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_request_id' is set
        if ('x_request_id' not in params or
                params['x_request_id'] is None):
            raise ValueError("Missing the required parameter `x_request_id` when calling `get_object_storage_credentials`")  # noqa: E501
        # verify the required parameter 'user_id' is set
        if ('user_id' not in params or
                params['user_id'] is None):
            raise ValueError("Missing the required parameter `user_id` when calling `get_object_storage_credentials`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'user_id' in params:
            path_params['userId'] = params['user_id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'x_request_id' in params:
            header_params['x-request-id'] = params['x_request_id']  # noqa: E501
        if 'x_trace_id' in params:
            header_params['x-trace-id'] = params['x_trace_id']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v1/users/{userId}/object-storages/credentials', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CredentialResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def regenerate_credentials(self, x_request_id, user_id, **kwargs):  # noqa: E501
        """Regenerates secret key of specified user for the S3 compatible object storages  # noqa: E501

        Regenerates secret key of specified user for the S3 compatible object storages. Please note that these credentials are valid for all object storages at different locations.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.regenerate_credentials(x_request_id, user_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_request_id: [Uuid4](https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)) to identify individual requests for support cases. You can use [uuidgenerator](https://www.uuidgenerator.net/version4) to generate them manually. (required)
        :param str user_id: The identifier of the user (required)
        :param str x_trace_id: Identifier to trace group of requests.
        :return: CredentialResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.regenerate_credentials_with_http_info(x_request_id, user_id, **kwargs)  # noqa: E501
        else:
            (data) = self.regenerate_credentials_with_http_info(x_request_id, user_id, **kwargs)  # noqa: E501
            return data

    def regenerate_credentials_with_http_info(self, x_request_id, user_id, **kwargs):  # noqa: E501
        """Regenerates secret key of specified user for the S3 compatible object storages  # noqa: E501

        Regenerates secret key of specified user for the S3 compatible object storages. Please note that these credentials are valid for all object storages at different locations.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.regenerate_credentials_with_http_info(x_request_id, user_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_request_id: [Uuid4](https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)) to identify individual requests for support cases. You can use [uuidgenerator](https://www.uuidgenerator.net/version4) to generate them manually. (required)
        :param str user_id: The identifier of the user (required)
        :param str x_trace_id: Identifier to trace group of requests.
        :return: CredentialResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_request_id', 'user_id', 'x_trace_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method regenerate_credentials" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_request_id' is set
        if ('x_request_id' not in params or
                params['x_request_id'] is None):
            raise ValueError("Missing the required parameter `x_request_id` when calling `regenerate_credentials`")  # noqa: E501
        # verify the required parameter 'user_id' is set
        if ('user_id' not in params or
                params['user_id'] is None):
            raise ValueError("Missing the required parameter `user_id` when calling `regenerate_credentials`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'user_id' in params:
            path_params['userId'] = params['user_id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'x_request_id' in params:
            header_params['x-request-id'] = params['x_request_id']  # noqa: E501
        if 'x_trace_id' in params:
            header_params['x-trace-id'] = params['x_trace_id']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v1/users/{userId}/object-storages/credentials', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CredentialResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def retrieve_user_is_password_set(self, x_request_id, **kwargs):  # noqa: E501
        """Get user is password set status  # noqa: E501

        Get info about idm user if the password is set.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.retrieve_user_is_password_set(x_request_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_request_id: [Uuid4](https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)) to identify individual requests for support cases. You can use [uuidgenerator](https://www.uuidgenerator.net/version4) to generate them manually. (required)
        :param str x_trace_id: Identifier to trace group of requests.
        :param str user_id: The user ID for checking if password is set for him
        :return: FindUserIsPasswordSetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.retrieve_user_is_password_set_with_http_info(x_request_id, **kwargs)  # noqa: E501
        else:
            (data) = self.retrieve_user_is_password_set_with_http_info(x_request_id, **kwargs)  # noqa: E501
            return data

    def retrieve_user_is_password_set_with_http_info(self, x_request_id, **kwargs):  # noqa: E501
        """Get user is password set status  # noqa: E501

        Get info about idm user if the password is set.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.retrieve_user_is_password_set_with_http_info(x_request_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_request_id: [Uuid4](https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)) to identify individual requests for support cases. You can use [uuidgenerator](https://www.uuidgenerator.net/version4) to generate them manually. (required)
        :param str x_trace_id: Identifier to trace group of requests.
        :param str user_id: The user ID for checking if password is set for him
        :return: FindUserIsPasswordSetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_request_id', 'x_trace_id', 'user_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method retrieve_user_is_password_set" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_request_id' is set
        if ('x_request_id' not in params or
                params['x_request_id'] is None):
            raise ValueError("Missing the required parameter `x_request_id` when calling `retrieve_user_is_password_set`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'user_id' in params:
            query_params.append(('userId', params['user_id']))  # noqa: E501

        header_params = {}
        if 'x_request_id' in params:
            header_params['x-request-id'] = params['x_request_id']  # noqa: E501
        if 'x_trace_id' in params:
            header_params['x-trace-id'] = params['x_trace_id']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearer']  # noqa: E501

        return self.api_client.call_api(
            '/v1/users/is-password-set', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FindUserIsPasswordSetResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
