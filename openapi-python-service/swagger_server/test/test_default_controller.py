# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.payment_provider import PaymentProvider  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_payemnt_providers_get(self):
        """Test case for payemnt_providers_get

        
        """
        response = self.client.open(
            '/v1/payemnt_providers',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_payemnt_providers_post(self):
        """Test case for payemnt_providers_post

        
        """
        body = PaymentProvider()
        response = self.client.open(
            '/v1/payemnt_providers',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_payment_provider_provider_name_delete(self):
        """Test case for payment_provider_provider_name_delete

        
        """
        response = self.client.open(
            '/v1/payment_provider/{provider_name}'.format(provider_name='provider_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_payment_provider_provider_name_get(self):
        """Test case for payment_provider_provider_name_get

        
        """
        response = self.client.open(
            '/v1/payment_provider/{provider_name}'.format(provider_name='provider_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_payment_provider_provider_name_put(self):
        """Test case for payment_provider_provider_name_put

        
        """
        response = self.client.open(
            '/v1/payment_provider/{provider_name}'.format(provider_name='provider_name_example'),
            method='PUT')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
