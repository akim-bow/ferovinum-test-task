#!/usr/bin/env python3
import contextlib
import typing

import connexion
import sqlite3
import csv

from connexion import ConnexionMiddleware

from swagger_server import encoder
from pathlib import Path

HEADER_ROW_COUNT = 1


def init_schema(connection: sqlite3.Connection):
    is_product_prices_exist = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='client_fees';"
    ).fetchone() is not None

    if not is_product_prices_exist:
        connection.execute(
            "CREATE TABLE client_fees(clientId TEXT PRIMARY KEY, fee REAL);"
        )

        with open(Path(__file__ + '/../data/ClientFees.csv').resolve()) as client_fees_file:
            client_fees = list(csv.reader(client_fees_file))[HEADER_ROW_COUNT:]

            def fee_as_float(fee: str) -> float:
                """ fee is a percent string 45.00% """
                return float(fee[0:-1])

            client_fees_with_float_percents = map(lambda row: (row[0], fee_as_float(row[1])), client_fees)

            connection.executemany(
                "INSERT INTO client_fees values (?, ?)",
                client_fees_with_float_percents
            )

        print('Table client_fees created.')

    is_product_prices_exist = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='product_prices';"
    ).fetchone() is not None

    if not is_product_prices_exist:
        connection.execute(
            "CREATE TABLE product_prices(productId TEXT PRIMARY KEY, price REAL);"
        )

        with open(Path(__file__ + '/../data/ProductPrices.csv').resolve()) as product_prices_file:
            product_prices = list(csv.reader(product_prices_file))[HEADER_ROW_COUNT:]

            product_prices_with_float_prices = map(lambda row: (row[0], float(row[1])), product_prices)

            connection.executemany(
                "INSERT INTO product_prices values (?, ?)",
                product_prices_with_float_prices
            )

        print('Table product_prices created.')

    is_orders_exist = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='orders';"
    ).fetchone() is not None

    if not is_orders_exist:
        connection.execute(
            "CREATE TABLE orders(id INTEGER PRIMARY KEY AUTOINCREMENT, clientId TEXT, productId TEXT, type TEXT, quantity INTEGER, timestamp TEXT);"
        )

        connection.executemany(
            "INSERT INTO orders(clientId, productId, type, quantity, timestamp) values (?, ?, ?, ?, ?)",
            (
                ('C-1', 'P-1', 'buy', 1000, '2020-01-01T10:00:00Z'),
                ('C-2', 'P-3', 'buy', 2000, '2020-01-01T10:00:00Z'),
                ('C-1', 'P-2', 'buy', 500, '2020-01-01T10:00:00Z'),
                ('C-1', 'P-1', 'sell', 50, '2020-01-01T11:00:00Z'),
                ('C-1', 'P-1', 'sell', 100, '2020-02-01T10:00:00Z'),
                ('C-2', 'P-3', 'sell', 100, '2020-02-28T10:00:00Z'),
                ('C-1', 'P-2', 'sell', 250, '2020-06-15T10:00:00Z'),
                ('C-3', 'P-1', 'buy', 5000, '2020-12-01T10:00:00Z'),
                ('C-2', 'P-3', 'sell', 1900, '2021-01-01T10:00:00Z'),
                ('C-3', 'P-1', 'sell', 1, '2021-07-01T10:00:00Z'),
                ('C-1', 'P-2', 'sell', 249, '2022-01-01T10:00:00Z'),
                ('C-3', 'P-1', 'sell', 4999, '2022-12-01T10:00:00Z'),
            )
        )


@contextlib.asynccontextmanager
async def lifespan_handler(app: ConnexionMiddleware) -> typing.AsyncIterator:
    """Called at startup and shutdown, can yield state which will be available on the
     request."""
    # TODO: check_same_thread shouldn't be used in production environment. Instead, connection pool should be used.
    connection = sqlite3.connect("orders.db", autocommit=True, check_same_thread=False)
    init_schema(connection)
    yield {"db": connection}
    print('Closing db connection...')
    connection.close()


def main():
    app = connexion.FlaskApp(__name__, specification_dir='swagger/', lifespan=lifespan_handler)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Ferovinum Quant Developer Homework Assignment'},
                pythonic_params=True)
    app.run(port=8080)


if __name__ == '__main__':
    main()
