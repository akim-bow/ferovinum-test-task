# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.order_request import OrderRequest  # noqa: E501
from swagger_server.models.order_response import OrderResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestOrderController(BaseTestCase):
    """OrderController integration test stubs"""

    def test_post_order(self):
        """Test case for post_order

        
        """
        body = OrderRequest()
        response = self.client.open(
            '/order',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest

    unittest.main()
