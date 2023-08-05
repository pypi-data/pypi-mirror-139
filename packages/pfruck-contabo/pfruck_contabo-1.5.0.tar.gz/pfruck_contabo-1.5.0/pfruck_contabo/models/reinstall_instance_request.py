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

class ReinstallInstanceRequest(object):
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
        'image_id': 'str',
        'ssh_keys': 'list[int]',
        'root_password': 'int',
        'user_data': 'str'
    }

    attribute_map = {
        'image_id': 'imageId',
        'ssh_keys': 'sshKeys',
        'root_password': 'rootPassword',
        'user_data': 'userData'
    }

    def __init__(self, image_id=None, ssh_keys=None, root_password=None, user_data=None):  # noqa: E501
        """ReinstallInstanceRequest - a model defined in Swagger"""  # noqa: E501
        self._image_id = None
        self._ssh_keys = None
        self._root_password = None
        self._user_data = None
        self.discriminator = None
        self.image_id = image_id
        if ssh_keys is not None:
            self.ssh_keys = ssh_keys
        if root_password is not None:
            self.root_password = root_password
        if user_data is not None:
            self.user_data = user_data

    @property
    def image_id(self):
        """Gets the image_id of this ReinstallInstanceRequest.  # noqa: E501

        ImageId to be used to setup the compute instance.  # noqa: E501

        :return: The image_id of this ReinstallInstanceRequest.  # noqa: E501
        :rtype: str
        """
        return self._image_id

    @image_id.setter
    def image_id(self, image_id):
        """Sets the image_id of this ReinstallInstanceRequest.

        ImageId to be used to setup the compute instance.  # noqa: E501

        :param image_id: The image_id of this ReinstallInstanceRequest.  # noqa: E501
        :type: str
        """
        if image_id is None:
            raise ValueError("Invalid value for `image_id`, must not be `None`")  # noqa: E501

        self._image_id = image_id

    @property
    def ssh_keys(self):
        """Gets the ssh_keys of this ReinstallInstanceRequest.  # noqa: E501

        Array of ids of public SSH Keys in order to access as admin user with root privileges (via sudo). Applies to Linux/BSD systems. Please refer to Secrets Management API.  # noqa: E501

        :return: The ssh_keys of this ReinstallInstanceRequest.  # noqa: E501
        :rtype: list[int]
        """
        return self._ssh_keys

    @ssh_keys.setter
    def ssh_keys(self, ssh_keys):
        """Sets the ssh_keys of this ReinstallInstanceRequest.

        Array of ids of public SSH Keys in order to access as admin user with root privileges (via sudo). Applies to Linux/BSD systems. Please refer to Secrets Management API.  # noqa: E501

        :param ssh_keys: The ssh_keys of this ReinstallInstanceRequest.  # noqa: E501
        :type: list[int]
        """

        self._ssh_keys = ssh_keys

    @property
    def root_password(self):
        """Gets the root_password of this ReinstallInstanceRequest.  # noqa: E501

        Password id for admin user with administrator/root privileges. For Linux/BSD please use SSH, for Windows RDP. Please refer to Secrets Management API.  # noqa: E501

        :return: The root_password of this ReinstallInstanceRequest.  # noqa: E501
        :rtype: int
        """
        return self._root_password

    @root_password.setter
    def root_password(self, root_password):
        """Sets the root_password of this ReinstallInstanceRequest.

        Password id for admin user with administrator/root privileges. For Linux/BSD please use SSH, for Windows RDP. Please refer to Secrets Management API.  # noqa: E501

        :param root_password: The root_password of this ReinstallInstanceRequest.  # noqa: E501
        :type: int
        """

        self._root_password = root_password

    @property
    def user_data(self):
        """Gets the user_data of this ReinstallInstanceRequest.  # noqa: E501

        [Cloud-Init](https://cloud-init.io/) Config in order to customize during start of compute instance.  # noqa: E501

        :return: The user_data of this ReinstallInstanceRequest.  # noqa: E501
        :rtype: str
        """
        return self._user_data

    @user_data.setter
    def user_data(self, user_data):
        """Sets the user_data of this ReinstallInstanceRequest.

        [Cloud-Init](https://cloud-init.io/) Config in order to customize during start of compute instance.  # noqa: E501

        :param user_data: The user_data of this ReinstallInstanceRequest.  # noqa: E501
        :type: str
        """

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
        if issubclass(ReinstallInstanceRequest, dict):
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
        if not isinstance(other, ReinstallInstanceRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
