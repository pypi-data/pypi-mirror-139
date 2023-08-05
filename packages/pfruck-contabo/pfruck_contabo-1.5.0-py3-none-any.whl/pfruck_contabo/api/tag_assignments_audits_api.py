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


class TagAssignmentsAuditsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def retrieve_assignments_audits_list(self, x_request_id, **kwargs):  # noqa: E501
        """List history about your assignments (audit)  # noqa: E501

        List and filters the history about your assignments.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.retrieve_assignments_audits_list(x_request_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_request_id: [Uuid4](https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)) to identify individual requests for support cases. You can use [uuidgenerator](https://www.uuidgenerator.net/version4) to generate them manually. (required)
        :param str x_trace_id: Identifier to trace group of requests.
        :param int page: Number of page to be fetched.
        :param int size: Number of elements per page.
        :param list[str] order_by: Specify fields and ordering (ASC for ascending, DESC for descending) in following format `field:ASC|DESC`.
        :param int tag_id: The identifier of the tag.
        :param str resource_id: The identifier of the resource.
        :param str request_id: The requestId of the API call which led to the change.
        :param str changed_by: UserId of the user which led to the change.
        :return: ListAssignmentAuditsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.retrieve_assignments_audits_list_with_http_info(x_request_id, **kwargs)  # noqa: E501
        else:
            (data) = self.retrieve_assignments_audits_list_with_http_info(x_request_id, **kwargs)  # noqa: E501
            return data

    def retrieve_assignments_audits_list_with_http_info(self, x_request_id, **kwargs):  # noqa: E501
        """List history about your assignments (audit)  # noqa: E501

        List and filters the history about your assignments.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.retrieve_assignments_audits_list_with_http_info(x_request_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_request_id: [Uuid4](https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)) to identify individual requests for support cases. You can use [uuidgenerator](https://www.uuidgenerator.net/version4) to generate them manually. (required)
        :param str x_trace_id: Identifier to trace group of requests.
        :param int page: Number of page to be fetched.
        :param int size: Number of elements per page.
        :param list[str] order_by: Specify fields and ordering (ASC for ascending, DESC for descending) in following format `field:ASC|DESC`.
        :param int tag_id: The identifier of the tag.
        :param str resource_id: The identifier of the resource.
        :param str request_id: The requestId of the API call which led to the change.
        :param str changed_by: UserId of the user which led to the change.
        :return: ListAssignmentAuditsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_request_id', 'x_trace_id', 'page', 'size', 'order_by', 'tag_id', 'resource_id', 'request_id', 'changed_by']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method retrieve_assignments_audits_list" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_request_id' is set
        if ('x_request_id' not in params or
                params['x_request_id'] is None):
            raise ValueError("Missing the required parameter `x_request_id` when calling `retrieve_assignments_audits_list`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'size' in params:
            query_params.append(('size', params['size']))  # noqa: E501
        if 'order_by' in params:
            query_params.append(('orderBy', params['order_by']))  # noqa: E501
            collection_formats['orderBy'] = 'multi'  # noqa: E501
        if 'tag_id' in params:
            query_params.append(('tagId', params['tag_id']))  # noqa: E501
        if 'resource_id' in params:
            query_params.append(('resourceId', params['resource_id']))  # noqa: E501
        if 'request_id' in params:
            query_params.append(('requestId', params['request_id']))  # noqa: E501
        if 'changed_by' in params:
            query_params.append(('changedBy', params['changed_by']))  # noqa: E501

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
            '/v1/tags/assignments/audits', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ListAssignmentAuditsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
