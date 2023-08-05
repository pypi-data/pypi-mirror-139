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
from pfruck_contabo.api.users_api import UsersApi  # noqa: E501
from pfruck_contabo.rest import ApiException


class TestUsersApi(unittest.TestCase):
    """UsersApi unit test stubs"""

    def setUp(self):
        self.api = UsersApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_user(self):
        """Test case for create_user

        Create a new user  # noqa: E501
        """
        pass

    def test_delete_user(self):
        """Test case for delete_user

        Delete existing user by id  # noqa: E501
        """
        pass

    def test_generate_client_secret(self):
        """Test case for generate_client_secret

        Generate new client secret  # noqa: E501
        """
        pass

    def test_resend_email_verification(self):
        """Test case for resend_email_verification

        Resend email verification  # noqa: E501
        """
        pass

    def test_reset_password(self):
        """Test case for reset_password

        Send reset password email  # noqa: E501
        """
        pass

    def test_retrieve_user(self):
        """Test case for retrieve_user

        Get specific user by id  # noqa: E501
        """
        pass

    def test_retrieve_user_client(self):
        """Test case for retrieve_user_client

        Get client  # noqa: E501
        """
        pass

    def test_retrieve_user_list(self):
        """Test case for retrieve_user_list

        List users  # noqa: E501
        """
        pass

    def test_update_user(self):
        """Test case for update_user

        Update specific user by id  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
