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

class UserAuditResponse(object):
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
        'id': 'int',
        'action': 'str',
        'timestamp': 'datetime',
        'tenant_id': 'str',
        'customer_id': 'str',
        'changed_by': 'str',
        'username': 'str',
        'request_id': 'str',
        'trace_id': 'str',
        'user_id': 'str',
        'changes': 'object'
    }

    attribute_map = {
        'id': 'id',
        'action': 'action',
        'timestamp': 'timestamp',
        'tenant_id': 'tenantId',
        'customer_id': 'customerId',
        'changed_by': 'changedBy',
        'username': 'username',
        'request_id': 'requestId',
        'trace_id': 'traceId',
        'user_id': 'userId',
        'changes': 'changes'
    }

    def __init__(self, id=None, action=None, timestamp=None, tenant_id=None, customer_id=None, changed_by=None, username=None, request_id=None, trace_id=None, user_id=None, changes=None):  # noqa: E501
        """UserAuditResponse - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._action = None
        self._timestamp = None
        self._tenant_id = None
        self._customer_id = None
        self._changed_by = None
        self._username = None
        self._request_id = None
        self._trace_id = None
        self._user_id = None
        self._changes = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if action is not None:
            self.action = action
        if timestamp is not None:
            self.timestamp = timestamp
        if tenant_id is not None:
            self.tenant_id = tenant_id
        if customer_id is not None:
            self.customer_id = customer_id
        if changed_by is not None:
            self.changed_by = changed_by
        if username is not None:
            self.username = username
        if request_id is not None:
            self.request_id = request_id
        if trace_id is not None:
            self.trace_id = trace_id
        if user_id is not None:
            self.user_id = user_id
        if changes is not None:
            if changes is not None:
                self.changes = changes

    @property
    def id(self):
        """Gets the id of this UserAuditResponse.  # noqa: E501

        The identifier of the audit entry.  # noqa: E501

        :return: The id of this UserAuditResponse.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this UserAuditResponse.

        The identifier of the audit entry.  # noqa: E501

        :param id: The id of this UserAuditResponse.  # noqa: E501
        :type: int
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def action(self):
        """Gets the action of this UserAuditResponse.  # noqa: E501

        Type of the action.  # noqa: E501

        :return: The action of this UserAuditResponse.  # noqa: E501
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this UserAuditResponse.

        Type of the action.  # noqa: E501

        :param action: The action of this UserAuditResponse.  # noqa: E501
        :type: str
        """
        if action is None:
            raise ValueError("Invalid value for `action`, must not be `None`")  # noqa: E501
        allowed_values = ["CREATED", "UPDATED", "DELETED"]  # noqa: E501
        if action not in allowed_values:
            raise ValueError(
                "Invalid value for `action` ({0}), must be one of {1}"  # noqa: E501
                .format(action, allowed_values)
            )

        self._action = action

    @property
    def timestamp(self):
        """Gets the timestamp of this UserAuditResponse.  # noqa: E501

        When the change took place.  # noqa: E501

        :return: The timestamp of this UserAuditResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this UserAuditResponse.

        When the change took place.  # noqa: E501

        :param timestamp: The timestamp of this UserAuditResponse.  # noqa: E501
        :type: datetime
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")  # noqa: E501

        self._timestamp = timestamp

    @property
    def tenant_id(self):
        """Gets the tenant_id of this UserAuditResponse.  # noqa: E501

        Customer tenant id  # noqa: E501

        :return: The tenant_id of this UserAuditResponse.  # noqa: E501
        :rtype: str
        """
        return self._tenant_id

    @tenant_id.setter
    def tenant_id(self, tenant_id):
        """Sets the tenant_id of this UserAuditResponse.

        Customer tenant id  # noqa: E501

        :param tenant_id: The tenant_id of this UserAuditResponse.  # noqa: E501
        :type: str
        """
        if tenant_id is None:
            raise ValueError("Invalid value for `tenant_id`, must not be `None`")  # noqa: E501

        self._tenant_id = tenant_id

    @property
    def customer_id(self):
        """Gets the customer_id of this UserAuditResponse.  # noqa: E501

        Customer number  # noqa: E501

        :return: The customer_id of this UserAuditResponse.  # noqa: E501
        :rtype: str
        """
        return self._customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        """Sets the customer_id of this UserAuditResponse.

        Customer number  # noqa: E501

        :param customer_id: The customer_id of this UserAuditResponse.  # noqa: E501
        :type: str
        """
        if customer_id is None:
            raise ValueError("Invalid value for `customer_id`, must not be `None`")  # noqa: E501

        self._customer_id = customer_id

    @property
    def changed_by(self):
        """Gets the changed_by of this UserAuditResponse.  # noqa: E501

        User ID  # noqa: E501

        :return: The changed_by of this UserAuditResponse.  # noqa: E501
        :rtype: str
        """
        return self._changed_by

    @changed_by.setter
    def changed_by(self, changed_by):
        """Sets the changed_by of this UserAuditResponse.

        User ID  # noqa: E501

        :param changed_by: The changed_by of this UserAuditResponse.  # noqa: E501
        :type: str
        """
        if changed_by is None:
            raise ValueError("Invalid value for `changed_by`, must not be `None`")  # noqa: E501

        self._changed_by = changed_by

    @property
    def username(self):
        """Gets the username of this UserAuditResponse.  # noqa: E501

        Name of the user which led to the change.  # noqa: E501

        :return: The username of this UserAuditResponse.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this UserAuditResponse.

        Name of the user which led to the change.  # noqa: E501

        :param username: The username of this UserAuditResponse.  # noqa: E501
        :type: str
        """
        if username is None:
            raise ValueError("Invalid value for `username`, must not be `None`")  # noqa: E501

        self._username = username

    @property
    def request_id(self):
        """Gets the request_id of this UserAuditResponse.  # noqa: E501

        The requestId of the API call which led to the change.  # noqa: E501

        :return: The request_id of this UserAuditResponse.  # noqa: E501
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """Sets the request_id of this UserAuditResponse.

        The requestId of the API call which led to the change.  # noqa: E501

        :param request_id: The request_id of this UserAuditResponse.  # noqa: E501
        :type: str
        """
        if request_id is None:
            raise ValueError("Invalid value for `request_id`, must not be `None`")  # noqa: E501

        self._request_id = request_id

    @property
    def trace_id(self):
        """Gets the trace_id of this UserAuditResponse.  # noqa: E501

        The traceId of the API call which led to the change.  # noqa: E501

        :return: The trace_id of this UserAuditResponse.  # noqa: E501
        :rtype: str
        """
        return self._trace_id

    @trace_id.setter
    def trace_id(self, trace_id):
        """Sets the trace_id of this UserAuditResponse.

        The traceId of the API call which led to the change.  # noqa: E501

        :param trace_id: The trace_id of this UserAuditResponse.  # noqa: E501
        :type: str
        """
        if trace_id is None:
            raise ValueError("Invalid value for `trace_id`, must not be `None`")  # noqa: E501

        self._trace_id = trace_id

    @property
    def user_id(self):
        """Gets the user_id of this UserAuditResponse.  # noqa: E501

        The identifier of the user  # noqa: E501

        :return: The user_id of this UserAuditResponse.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this UserAuditResponse.

        The identifier of the user  # noqa: E501

        :param user_id: The user_id of this UserAuditResponse.  # noqa: E501
        :type: str
        """
        if user_id is None:
            raise ValueError("Invalid value for `user_id`, must not be `None`")  # noqa: E501

        self._user_id = user_id

    @property
    def changes(self):
        """Gets the changes of this UserAuditResponse.  # noqa: E501

        List of actual changes.  # noqa: E501

        :return: The changes of this UserAuditResponse.  # noqa: E501
        :rtype: object
        """
        return self._changes

    @changes.setter
    def changes(self, changes):
        """Sets the changes of this UserAuditResponse.

        List of actual changes.  # noqa: E501

        :param changes: The changes of this UserAuditResponse.  # noqa: E501
        :type: object
        """

        self._changes = changes

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
        if issubclass(UserAuditResponse, dict):
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
        if not isinstance(other, UserAuditResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
