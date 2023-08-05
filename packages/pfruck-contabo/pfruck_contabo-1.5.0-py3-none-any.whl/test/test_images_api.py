# coding: utf-8

"""
    Contabo API


    OpenAPI spec version: 1.0.0
    Contact: support@contabo.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import pfruck_contabo
from pfruck_contabo.api.images_api import ImagesApi  # noqa: E501
from pfruck_contabo.rest import ApiException


class TestImagesApi(unittest.TestCase):
    """ImagesApi unit test stubs"""

    def setUp(self):
        self.api = ImagesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_custom_image(self):
        """Test case for create_custom_image

        Provide a custom image  # noqa: E501
        """
        pass

    def test_delete_image(self):
        """Test case for delete_image

        Delete an uploaded custom image by its id  # noqa: E501
        """
        pass

    def test_retrieve_custom_images_stats(self):
        """Test case for retrieve_custom_images_stats

        List statistics regarding the customer's custom images  # noqa: E501
        """
        pass

    def test_retrieve_image(self):
        """Test case for retrieve_image

        Get details about a specific image by its id  # noqa: E501
        """
        pass

    def test_retrieve_image_list(self):
        """Test case for retrieve_image_list

        List available standard and custom images  # noqa: E501
        """
        pass

    def test_update_image(self):
        """Test case for update_image

        Update custom image name by its id  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
