# coding: utf-8

"""
    Contabo API


    OpenAPI spec version: 1.0.0
    Contact: support@contabo.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class ListRoleResponse(object):
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
        'pagination': 'AllOfListRoleResponsePagination',
        'data': 'list[RoleResponse]',
        'links': 'AllOfListRoleResponseLinks'
    }

    attribute_map = {
        'pagination': '_pagination',
        'data': 'data',
        'links': '_links'
    }

    def __init__(self, pagination=None, data=None, links=None):  # noqa: E501
        """ListRoleResponse - a model defined in Swagger"""  # noqa: E501
        self._pagination = None
        self._data = None
        self._links = None
        self.discriminator = None
        if pagination is not None:
            self.pagination = pagination
        if data is not None:
            self.data = data
        if links is not None:
            self.links = links

    @property
    def pagination(self):
        """Gets the pagination of this ListRoleResponse.  # noqa: E501

        Data about pagination like how many results, pages, page size.  # noqa: E501

        :return: The pagination of this ListRoleResponse.  # noqa: E501
        :rtype: AllOfListRoleResponsePagination
        """
        return self._pagination

    @pagination.setter
    def pagination(self, pagination):
        """Sets the pagination of this ListRoleResponse.

        Data about pagination like how many results, pages, page size.  # noqa: E501

        :param pagination: The pagination of this ListRoleResponse.  # noqa: E501
        :type: AllOfListRoleResponsePagination
        """
        if pagination is None:
            raise ValueError("Invalid value for `pagination`, must not be `None`")  # noqa: E501

        self._pagination = pagination

    @property
    def data(self):
        """Gets the data of this ListRoleResponse.  # noqa: E501


        :return: The data of this ListRoleResponse.  # noqa: E501
        :rtype: list[RoleResponse]
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this ListRoleResponse.


        :param data: The data of this ListRoleResponse.  # noqa: E501
        :type: list[RoleResponse]
        """
        if data is None:
            raise ValueError("Invalid value for `data`, must not be `None`")  # noqa: E501

        self._data = data

    @property
    def links(self):
        """Gets the links of this ListRoleResponse.  # noqa: E501


        :return: The links of this ListRoleResponse.  # noqa: E501
        :rtype: AllOfListRoleResponseLinks
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this ListRoleResponse.


        :param links: The links of this ListRoleResponse.  # noqa: E501
        :type: AllOfListRoleResponseLinks
        """
        if links is None:
            raise ValueError("Invalid value for `links`, must not be `None`")  # noqa: E501

        self._links = links

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
        if issubclass(ListRoleResponse, dict):
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
        if not isinstance(other, ListRoleResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
