# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.balance import Balance  # noqa: E501
from swagger_server.models.portfolio import Portfolio  # noqa: E501
from swagger_server.models.transaction import Transaction  # noqa: E501
from swagger_server.test import BaseTestCase


class TestQueryController(BaseTestCase):
    """QueryController integration test stubs"""

    def test_get_balance_by_client(self):
        """Test case for get_balance_by_client

        
        """
        query_string = [('_date', '2013-10-20')]
        response = self.client.open(
            '/balance/client/{clientId}'.format(client_id='client_id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_balance_by_product(self):
        """Test case for get_balance_by_product

        
        """
        query_string = [('_date', '2013-10-20')]
        response = self.client.open(
            '/balance/product/{productId}'.format(product_id='product_id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_portfolio_by_client(self):
        """Test case for get_portfolio_by_client

        
        """
        query_string = [('_date', '2013-10-20')]
        response = self.client.open(
            '/portfolio/client/{clientId}'.format(client_id='client_id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_transactions_by_client(self):
        """Test case for get_transactions_by_client

        
        """
        query_string = [('from_date', '2013-10-20'),
                        ('to_date', '2013-10-20')]
        response = self.client.open(
            '/transactions/client/{clientId}'.format(client_id='client_id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_transactions_by_product(self):
        """Test case for get_transactions_by_product

        
        """
        query_string = [('from_date', '2013-10-20'),
                        ('to_date', '2013-10-20')]
        response = self.client.open(
            '/transactions/product/{productId}'.format(product_id='product_id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest

    unittest.main()
