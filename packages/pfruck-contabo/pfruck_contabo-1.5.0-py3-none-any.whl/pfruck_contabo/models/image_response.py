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

class ImageResponse(object):
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
        'tenant_id': 'str',
        'customer_id': 'str',
        'name': 'str',
        'description': 'str',
        'url': 'str',
        'size_mb': 'float',
        'uploaded_size_mb': 'float',
        'os_type': 'str',
        'version': 'str',
        'format': 'str',
        'status': 'str',
        'error_message': 'str',
        'standard_image': 'bool',
        'creation_date': 'datetime',
        'last_modified_date': 'datetime'
    }

    attribute_map = {
        'image_id': 'imageId',
        'tenant_id': 'tenantId',
        'customer_id': 'customerId',
        'name': 'name',
        'description': 'description',
        'url': 'url',
        'size_mb': 'sizeMb',
        'uploaded_size_mb': 'uploadedSizeMb',
        'os_type': 'osType',
        'version': 'version',
        'format': 'format',
        'status': 'status',
        'error_message': 'errorMessage',
        'standard_image': 'standardImage',
        'creation_date': 'creationDate',
        'last_modified_date': 'lastModifiedDate'
    }

    def __init__(self, image_id=None, tenant_id=None, customer_id=None, name=None, description=None, url=None, size_mb=None, uploaded_size_mb=None, os_type=None, version=None, format=None, status=None, error_message=None, standard_image=None, creation_date=None, last_modified_date=None):  # noqa: E501
        """ImageResponse - a model defined in Swagger"""  # noqa: E501
        self._image_id = None
        self._tenant_id = None
        self._customer_id = None
        self._name = None
        self._description = None
        self._url = None
        self._size_mb = None
        self._uploaded_size_mb = None
        self._os_type = None
        self._version = None
        self._format = None
        self._status = None
        self._error_message = None
        self._standard_image = None
        self._creation_date = None
        self._last_modified_date = None
        self.discriminator = None
        if image_id is not None:
            self.image_id = image_id
        if tenant_id is not None:
            self.tenant_id = tenant_id
        if customer_id is not None:
            self.customer_id = customer_id
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if url is not None:
            self.url = url
        if size_mb is not None:
            self.size_mb = size_mb
        if uploaded_size_mb is not None:
            self.uploaded_size_mb = uploaded_size_mb
        if os_type is not None:
            self.os_type = os_type
        if version is not None:
            self.version = version
        if format is not None:
            self.format = format
        if status is not None:
            self.status = status
        if error_message is not None:
            self.error_message = error_message
        if standard_image is not None:
            self.standard_image = standard_image
        if creation_date is not None:
            self.creation_date = creation_date
        if last_modified_date is not None:
            self.last_modified_date = last_modified_date

    @property
    def image_id(self):
        """Gets the image_id of this ImageResponse.  # noqa: E501

        Image's id  # noqa: E501

        :return: The image_id of this ImageResponse.  # noqa: E501
        :rtype: str
        """
        return self._image_id

    @image_id.setter
    def image_id(self, image_id):
        """Sets the image_id of this ImageResponse.

        Image's id  # noqa: E501

        :param image_id: The image_id of this ImageResponse.  # noqa: E501
        :type: str
        """
        if image_id is None:
            raise ValueError("Invalid value for `image_id`, must not be `None`")  # noqa: E501

        self._image_id = image_id

    @property
    def tenant_id(self):
        """Gets the tenant_id of this ImageResponse.  # noqa: E501

        Your customer tenant id  # noqa: E501

        :return: The tenant_id of this ImageResponse.  # noqa: E501
        :rtype: str
        """
        return self._tenant_id

    @tenant_id.setter
    def tenant_id(self, tenant_id):
        """Sets the tenant_id of this ImageResponse.

        Your customer tenant id  # noqa: E501

        :param tenant_id: The tenant_id of this ImageResponse.  # noqa: E501
        :type: str
        """
        if tenant_id is None:
            raise ValueError("Invalid value for `tenant_id`, must not be `None`")  # noqa: E501
        allowed_values = ["DE", "INT"]  # noqa: E501
        if tenant_id not in allowed_values:
            raise ValueError(
                "Invalid value for `tenant_id` ({0}), must be one of {1}"  # noqa: E501
                .format(tenant_id, allowed_values)
            )

        self._tenant_id = tenant_id

    @property
    def customer_id(self):
        """Gets the customer_id of this ImageResponse.  # noqa: E501

        Customer ID  # noqa: E501

        :return: The customer_id of this ImageResponse.  # noqa: E501
        :rtype: str
        """
        return self._customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        """Sets the customer_id of this ImageResponse.

        Customer ID  # noqa: E501

        :param customer_id: The customer_id of this ImageResponse.  # noqa: E501
        :type: str
        """
        if customer_id is None:
            raise ValueError("Invalid value for `customer_id`, must not be `None`")  # noqa: E501

        self._customer_id = customer_id

    @property
    def name(self):
        """Gets the name of this ImageResponse.  # noqa: E501

        Image Name  # noqa: E501

        :return: The name of this ImageResponse.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ImageResponse.

        Image Name  # noqa: E501

        :param name: The name of this ImageResponse.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this ImageResponse.  # noqa: E501

        Image Description  # noqa: E501

        :return: The description of this ImageResponse.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ImageResponse.

        Image Description  # noqa: E501

        :param description: The description of this ImageResponse.  # noqa: E501
        :type: str
        """
        if description is None:
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501

        self._description = description

    @property
    def url(self):
        """Gets the url of this ImageResponse.  # noqa: E501

        URL from where the image has been downloaded / provided.  # noqa: E501

        :return: The url of this ImageResponse.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this ImageResponse.

        URL from where the image has been downloaded / provided.  # noqa: E501

        :param url: The url of this ImageResponse.  # noqa: E501
        :type: str
        """
        if url is None:
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501

        self._url = url

    @property
    def size_mb(self):
        """Gets the size_mb of this ImageResponse.  # noqa: E501

        Image Size in MB  # noqa: E501

        :return: The size_mb of this ImageResponse.  # noqa: E501
        :rtype: float
        """
        return self._size_mb

    @size_mb.setter
    def size_mb(self, size_mb):
        """Sets the size_mb of this ImageResponse.

        Image Size in MB  # noqa: E501

        :param size_mb: The size_mb of this ImageResponse.  # noqa: E501
        :type: float
        """
        if size_mb is None:
            raise ValueError("Invalid value for `size_mb`, must not be `None`")  # noqa: E501

        self._size_mb = size_mb

    @property
    def uploaded_size_mb(self):
        """Gets the uploaded_size_mb of this ImageResponse.  # noqa: E501

        Image Uploaded Size in MB  # noqa: E501

        :return: The uploaded_size_mb of this ImageResponse.  # noqa: E501
        :rtype: float
        """
        return self._uploaded_size_mb

    @uploaded_size_mb.setter
    def uploaded_size_mb(self, uploaded_size_mb):
        """Sets the uploaded_size_mb of this ImageResponse.

        Image Uploaded Size in MB  # noqa: E501

        :param uploaded_size_mb: The uploaded_size_mb of this ImageResponse.  # noqa: E501
        :type: float
        """
        if uploaded_size_mb is None:
            raise ValueError("Invalid value for `uploaded_size_mb`, must not be `None`")  # noqa: E501

        self._uploaded_size_mb = uploaded_size_mb

    @property
    def os_type(self):
        """Gets the os_type of this ImageResponse.  # noqa: E501

        Type of operating system (OS)  # noqa: E501

        :return: The os_type of this ImageResponse.  # noqa: E501
        :rtype: str
        """
        return self._os_type

    @os_type.setter
    def os_type(self, os_type):
        """Sets the os_type of this ImageResponse.

        Type of operating system (OS)  # noqa: E501

        :param os_type: The os_type of this ImageResponse.  # noqa: E501
        :type: str
        """
        if os_type is None:
            raise ValueError("Invalid value for `os_type`, must not be `None`")  # noqa: E501

        self._os_type = os_type

    @property
    def version(self):
        """Gets the version of this ImageResponse.  # noqa: E501

        Version number to distinguish the contents of an image. Could be the version of the operating system for example.  # noqa: E501

        :return: The version of this ImageResponse.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ImageResponse.

        Version number to distinguish the contents of an image. Could be the version of the operating system for example.  # noqa: E501

        :param version: The version of this ImageResponse.  # noqa: E501
        :type: str
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def format(self):
        """Gets the format of this ImageResponse.  # noqa: E501

        Image format  # noqa: E501

        :return: The format of this ImageResponse.  # noqa: E501
        :rtype: str
        """
        return self._format

    @format.setter
    def format(self, format):
        """Sets the format of this ImageResponse.

        Image format  # noqa: E501

        :param format: The format of this ImageResponse.  # noqa: E501
        :type: str
        """
        if format is None:
            raise ValueError("Invalid value for `format`, must not be `None`")  # noqa: E501
        allowed_values = ["iso", "qcow2"]  # noqa: E501
        if format not in allowed_values:
            raise ValueError(
                "Invalid value for `format` ({0}), must be one of {1}"  # noqa: E501
                .format(format, allowed_values)
            )

        self._format = format

    @property
    def status(self):
        """Gets the status of this ImageResponse.  # noqa: E501

        Image status (e.g. if image is still downloading)  # noqa: E501

        :return: The status of this ImageResponse.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ImageResponse.

        Image status (e.g. if image is still downloading)  # noqa: E501

        :param status: The status of this ImageResponse.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def error_message(self):
        """Gets the error_message of this ImageResponse.  # noqa: E501

        Image download error message  # noqa: E501

        :return: The error_message of this ImageResponse.  # noqa: E501
        :rtype: str
        """
        return self._error_message

    @error_message.setter
    def error_message(self, error_message):
        """Sets the error_message of this ImageResponse.

        Image download error message  # noqa: E501

        :param error_message: The error_message of this ImageResponse.  # noqa: E501
        :type: str
        """
        if error_message is None:
            raise ValueError("Invalid value for `error_message`, must not be `None`")  # noqa: E501

        self._error_message = error_message

    @property
    def standard_image(self):
        """Gets the standard_image of this ImageResponse.  # noqa: E501

        Flag indicating that image is either a standard (true) or a custom image (false)  # noqa: E501

        :return: The standard_image of this ImageResponse.  # noqa: E501
        :rtype: bool
        """
        return self._standard_image

    @standard_image.setter
    def standard_image(self, standard_image):
        """Sets the standard_image of this ImageResponse.

        Flag indicating that image is either a standard (true) or a custom image (false)  # noqa: E501

        :param standard_image: The standard_image of this ImageResponse.  # noqa: E501
        :type: bool
        """
        if standard_image is None:
            raise ValueError("Invalid value for `standard_image`, must not be `None`")  # noqa: E501

        self._standard_image = standard_image

    @property
    def creation_date(self):
        """Gets the creation_date of this ImageResponse.  # noqa: E501

        The creation date time for the image  # noqa: E501

        :return: The creation_date of this ImageResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        """Sets the creation_date of this ImageResponse.

        The creation date time for the image  # noqa: E501

        :param creation_date: The creation_date of this ImageResponse.  # noqa: E501
        :type: datetime
        """
        if creation_date is None:
            raise ValueError("Invalid value for `creation_date`, must not be `None`")  # noqa: E501

        self._creation_date = creation_date

    @property
    def last_modified_date(self):
        """Gets the last_modified_date of this ImageResponse.  # noqa: E501

        The last modified date time for the image  # noqa: E501

        :return: The last_modified_date of this ImageResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._last_modified_date

    @last_modified_date.setter
    def last_modified_date(self, last_modified_date):
        """Sets the last_modified_date of this ImageResponse.

        The last modified date time for the image  # noqa: E501

        :param last_modified_date: The last_modified_date of this ImageResponse.  # noqa: E501
        :type: datetime
        """
        if last_modified_date is None:
            raise ValueError("Invalid value for `last_modified_date`, must not be `None`")  # noqa: E501

        self._last_modified_date = last_modified_date

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
        if issubclass(ImageResponse, dict):
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
        if not isinstance(other, ImageResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
