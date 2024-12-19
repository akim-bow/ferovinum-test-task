from connexion import request
from sqlite3 import Connection

from swagger_server.models.order_request import OrderRequest  # noqa: E501
from swagger_server.models.order_response import OrderResponse  # noqa: E501
from swagger_server import util


def post_order(body):  # noqa: E501
    """post_order

    Submit new order request # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: OrderResponse
    """

    body = OrderRequest.from_dict(body)

    db: Connection = request.state.db

    # TODO: Ideally we should check that order is valid. For now we assume that all orders are valid.

    db.execute('INSERT INTO orders(clientId, productId, type, quantity, timestamp) values (?, ?, ?, ?, ?)', [
        body.client_id,
        body.product_id,
        body.type,
        body.quantity,
        body.timestamp
    ])

    return 'OK'
