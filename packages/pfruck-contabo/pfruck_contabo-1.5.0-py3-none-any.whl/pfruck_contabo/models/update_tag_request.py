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

class UpdateTagRequest(object):
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
        'name': 'str',
        'color': 'str'
    }

    attribute_map = {
        'name': 'name',
        'color': 'color'
    }

    def __init__(self, name=None, color=None):  # noqa: E501
        """UpdateTagRequest - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._color = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if color is not None:
            self.color = color

    @property
    def name(self):
        """Gets the name of this UpdateTagRequest.  # noqa: E501

        The name of the tag. Tags may contain letters, numbers, colons, dashes, and underscores. There is a limit of 255 characters per tag.  # noqa: E501

        :return: The name of this UpdateTagRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdateTagRequest.

        The name of the tag. Tags may contain letters, numbers, colons, dashes, and underscores. There is a limit of 255 characters per tag.  # noqa: E501

        :param name: The name of this UpdateTagRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def color(self):
        """Gets the color of this UpdateTagRequest.  # noqa: E501

        The color of the tag. Color can be specified using hexadecimal value. Default color is #0A78C3  # noqa: E501

        :return: The color of this UpdateTagRequest.  # noqa: E501
        :rtype: str
        """
        return self._color

    @color.setter
    def color(self, color):
        """Sets the color of this UpdateTagRequest.

        The color of the tag. Color can be specified using hexadecimal value. Default color is #0A78C3  # noqa: E501

        :param color: The color of this UpdateTagRequest.  # noqa: E501
        :type: str
        """

        self._color = color

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
        if issubclass(UpdateTagRequest, dict):
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
        if not isinstance(other, UpdateTagRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
