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

class CreateUserResponseData(object):
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
        'tenant_id': 'str',
        'customer_id': 'str',
        'user_id': 'str'
    }

    attribute_map = {
        'tenant_id': 'tenantId',
        'customer_id': 'customerId',
        'user_id': 'userId'
    }

    def __init__(self, tenant_id=None, customer_id=None, user_id=None):  # noqa: E501
        """CreateUserResponseData - a model defined in Swagger"""  # noqa: E501
        self._tenant_id = None
        self._customer_id = None
        self._user_id = None
        self.discriminator = None
        if tenant_id is not None:
            self.tenant_id = tenant_id
        if customer_id is not None:
            self.customer_id = customer_id
        if user_id is not None:
            self.user_id = user_id

    @property
    def tenant_id(self):
        """Gets the tenant_id of this CreateUserResponseData.  # noqa: E501

        Your customer tenant id  # noqa: E501

        :return: The tenant_id of this CreateUserResponseData.  # noqa: E501
        :rtype: str
        """
        return self._tenant_id

    @tenant_id.setter
    def tenant_id(self, tenant_id):
        """Sets the tenant_id of this CreateUserResponseData.

        Your customer tenant id  # noqa: E501

        :param tenant_id: The tenant_id of this CreateUserResponseData.  # noqa: E501
        :type: str
        """
        if tenant_id is None:
            raise ValueError("Invalid value for `tenant_id`, must not be `None`")  # noqa: E501

        self._tenant_id = tenant_id

    @property
    def customer_id(self):
        """Gets the customer_id of this CreateUserResponseData.  # noqa: E501

        Your customer number  # noqa: E501

        :return: The customer_id of this CreateUserResponseData.  # noqa: E501
        :rtype: str
        """
        return self._customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        """Sets the customer_id of this CreateUserResponseData.

        Your customer number  # noqa: E501

        :param customer_id: The customer_id of this CreateUserResponseData.  # noqa: E501
        :type: str
        """
        if customer_id is None:
            raise ValueError("Invalid value for `customer_id`, must not be `None`")  # noqa: E501

        self._customer_id = customer_id

    @property
    def user_id(self):
        """Gets the user_id of this CreateUserResponseData.  # noqa: E501

        User's id  # noqa: E501

        :return: The user_id of this CreateUserResponseData.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this CreateUserResponseData.

        User's id  # noqa: E501

        :param user_id: The user_id of this CreateUserResponseData.  # noqa: E501
        :type: str
        """
        if user_id is None:
            raise ValueError("Invalid value for `user_id`, must not be `None`")  # noqa: E501

        self._user_id = user_id

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
        if issubclass(CreateUserResponseData, dict):
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
        if not isinstance(other, CreateUserResponseData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
