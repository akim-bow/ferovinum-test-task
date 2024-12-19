# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class OrderRequest(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, client_id: str = None, product_id: str = None, quantity: int = None, timestamp: datetime = None,
                 type: str = None):  # noqa: E501
        """OrderRequest - a model defined in Swagger

        :param client_id: The client_id of this OrderRequest.  # noqa: E501
        :type client_id: str
        :param product_id: The product_id of this OrderRequest.  # noqa: E501
        :type product_id: str
        :param quantity: The quantity of this OrderRequest.  # noqa: E501
        :type quantity: int
        :param timestamp: The timestamp of this OrderRequest.  # noqa: E501
        :type timestamp: datetime
        :param type: The type of this OrderRequest.  # noqa: E501
        :type type: str
        """
        self.swagger_types = {
            'client_id': str,
            'product_id': str,
            'quantity': int,
            'timestamp': datetime,
            'type': str
        }

        self.attribute_map = {
            'client_id': 'clientId',
            'product_id': 'productId',
            'quantity': 'quantity',
            'timestamp': 'timestamp',
            'type': 'type'
        }
        self._client_id = client_id
        self._product_id = product_id
        self._quantity = quantity
        self._timestamp = timestamp
        self._type = type

    @classmethod
    def from_dict(cls, dikt) -> 'OrderRequest':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The OrderRequest of this OrderRequest.  # noqa: E501
        :rtype: OrderRequest
        """
        return util.deserialize_model(dikt, cls)

    @property
    def client_id(self) -> str:
        """Gets the client_id of this OrderRequest.

        Client Identifier  # noqa: E501

        :return: The client_id of this OrderRequest.
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id: str):
        """Sets the client_id of this OrderRequest.

        Client Identifier  # noqa: E501

        :param client_id: The client_id of this OrderRequest.
        :type client_id: str
        """

        self._client_id = client_id

    @property
    def product_id(self) -> str:
        """Gets the product_id of this OrderRequest.

        Product Identifier  # noqa: E501

        :return: The product_id of this OrderRequest.
        :rtype: str
        """
        return self._product_id

    @product_id.setter
    def product_id(self, product_id: str):
        """Sets the product_id of this OrderRequest.

        Product Identifier  # noqa: E501

        :param product_id: The product_id of this OrderRequest.
        :type product_id: str
        """

        self._product_id = product_id

    @property
    def quantity(self) -> int:
        """Gets the quantity of this OrderRequest.

        Number of Units  # noqa: E501

        :return: The quantity of this OrderRequest.
        :rtype: int
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: int):
        """Sets the quantity of this OrderRequest.

        Number of Units  # noqa: E501

        :param quantity: The quantity of this OrderRequest.
        :type quantity: int
        """

        self._quantity = quantity

    @property
    def timestamp(self) -> datetime:
        """Gets the timestamp of this OrderRequest.

        System Timestamp  # noqa: E501

        :return: The timestamp of this OrderRequest.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: datetime):
        """Sets the timestamp of this OrderRequest.

        System Timestamp  # noqa: E501

        :param timestamp: The timestamp of this OrderRequest.
        :type timestamp: datetime
        """

        self._timestamp = timestamp

    @property
    def type(self) -> str:
        """Gets the type of this OrderRequest.

        Buy/Sell  # noqa: E501

        :return: The type of this OrderRequest.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this OrderRequest.

        Buy/Sell  # noqa: E501

        :param type: The type of this OrderRequest.
        :type type: str
        """
        allowed_values = ["buy", "sell"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"
                .format(type, allowed_values)
            )

        self._type = type