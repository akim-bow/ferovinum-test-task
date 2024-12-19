from datetime import datetime, date as date_import
from dateutil.relativedelta import relativedelta
from sqlite3 import Connection

from connexion import request

from swagger_server import util


def get_balance_by_client(client_id, date=None):  # noqa: E501
    """get_balance_by_client

    Stock balance by client # noqa: E501

    :param client_id: Client Identifier
    :type client_id: str
    :param date: Date to reference result snapshot, default to today
    :type date: str

    :rtype: List[Balance]
    """

    db: Connection = request.state.db

    if date is None:
        orders = db.execute('SELECT * FROM orders WHERE clientId = ? ORDER BY timestamp ASC', [client_id])
    else:
        try:
            date = datetime.fromisoformat(date)
        except ValueError:
            return { 'message': 'Bad date param' }, 400

        orders = db.execute('SELECT * FROM orders WHERE clientId = ? and date(timestamp) <= date(?) ORDER BY timestamp ASC', [client_id, date])

    product_quantities: dict[str, int] = {}

    for order in orders:
        [_, _, product_id, type, quantity, _] = order

        if product_id not in product_quantities:
            product_quantities[product_id] = 0

        if type == 'sell':
            quantity = -quantity

        product_quantities[product_id] += quantity

    result = list(map(lambda k: (client_id, k, product_quantities[k]), product_quantities.keys()))

    return result


def get_balance_by_product(product_id, date=None):  # noqa: E501
    """get_balance_by_product

    Stock balance by product # noqa: E501

    :param product_id: Product Identifier
    :type product_id: str
    :param date: Date to reference result snapshot, default to today
    :type date: str

    :rtype: List[Balance]
    """

    db: Connection = request.state.db

    if date is None:
        orders = db.execute('SELECT * FROM orders WHERE productId = ? ORDER BY timestamp ASC', [product_id])
    else:
        try:
            date = datetime.fromisoformat(date)
        except ValueError:
            return {'message': 'Bad date param'}, 400

        orders = db.execute(
            'SELECT * FROM orders WHERE productId = ? and date(timestamp) <= date(?) ORDER BY timestamp ASC',
            [product_id, date])

    client_quantities: dict[str, int] = {}

    for order in orders:
        [_, client_id, _, type, quantity, _] = order

        if client_id not in client_quantities:
            client_quantities[client_id] = 0

        if type == 'sell':
            quantity = -quantity

        client_quantities[client_id] += quantity

    result = list(map(lambda k: (k, product_id, client_quantities[k]), client_quantities.keys()))

    return result


def get_portfolio_by_client(client_id, date=None):  # noqa: E501
    """get_portfolio_by_client

    Portfolio metrics by client # noqa: E501

    :param client_id: Client Identifier
    :type client_id: str
    :param date: Date to reference result snapshot, default to today
    :type date: str

    :rtype: List[Portfolio]
    """

    db: Connection = request.state.db

    if date is None:
        orders = db.execute('SELECT * FROM orders WHERE clientId = ? ORDER BY timestamp ASC', [client_id])
    else:
        try:
            date = datetime.fromisoformat(date)
        except ValueError:
            return {'message': 'Bad date param'}, 400

        orders = db.execute(
            'SELECT * FROM orders WHERE clientId = ? AND date(timestamp) <= date(?) ORDER BY timestamp ASC',
            [client_id, date])

    price_map: dict[str, float] = {}
    prices = db.execute('SELECT * FROM product_prices').fetchall()
    for price_entry in prices:
        [product_id, price] = price_entry
        price_map[product_id] = price

    # product id to timestamp to amount
    product_amounts: dict[str, dict[str, int]] = {}

    (_, client_percent) = db.execute('SELECT * FROM client_fees WHERE clientId = ?', [client_id]).fetchone()

    total_fees = 0
    total_product_amount = 0

    for order in orders:
        [_, _, product_id, type, quantity, timestamp] = order
        print(product_id, type, quantity, timestamp)

        if product_id not in product_amounts:
            product_amounts[product_id] = {}

        if type == 'buy':
            if timestamp not in product_amounts[product_id]:
                product_amounts[product_id][timestamp] = 0

            product_amounts[product_id][timestamp] = quantity

            price = price_map[product_id]
            total_product_amount += price * quantity
        else:
            amount = quantity
            while amount > 0:
                current_amounts = product_amounts[product_id]
                # There should always be a key because all orders are valid
                min_timestamp = min(current_amounts.keys())

                prev_amount_of_timestamp = current_amounts[min_timestamp]
                current_amounts[min_timestamp] -= min(current_amounts[min_timestamp], amount)
                product_delta = prev_amount_of_timestamp - current_amounts[min_timestamp]
                amount -= product_delta

                if current_amounts[min_timestamp] == 0:
                    del current_amounts[min_timestamp]

                difference = relativedelta(datetime.fromisoformat(timestamp), datetime.fromisoformat(min_timestamp))
                difference_in_months = difference.years * 12 + difference.months + 1

                price = price_map[product_id]
                fee_percent = (1 + (client_percent / 100) / 12) ** (12 * (difference_in_months / 12))
                price_with_fee = round(price * fee_percent, 2)

                total_fees += price_with_fee * product_delta - price * product_delta
                total_product_amount += price_with_fee * product_delta

    return {
        'lifeToDateFeeNotional': round(total_fees, 2),
        'lifeToDateProductNotional': round(total_product_amount, 2),
        # TODO: other params are unclear to me, not enough context in the docs.
    }


def get_transactions_by_client(client_id, from_date=None, to_date=None):  # noqa: E501
    """get_transactions_by_client

    Time-series of transactions by client # noqa: E501

    :param client_id: Client Identifier
    :type client_id: str
    :param from_date: Include transactions starting and including date, default to today
    :type from_date: str
    :param to_date: Include transactions ending and including date, default to today
    :type to_date: str

    :rtype: List[Transaction]
    """

    db: Connection = request.state.db

    for date_value in [from_date, to_date]:
        if date_value is None:
            continue

        try:
            datetime.fromisoformat(date_value)
        except ValueError:
            return {'message': 'Bad date param - ' + date_value}, 400

    condition = ''
    if to_date is not None:
        condition += ' and date(timestamp) <= date(?)'

    remove_none_values = lambda l: [x for x in l if x is not None]

    orders = db.execute(
        f'SELECT * FROM orders WHERE clientId = ? {condition} ORDER BY timestamp ASC',
        [client_id, *remove_none_values([to_date])])

    # Assuming that the client can buy only once!
    # But this is not mentioned in task description so calculating price is more complicated.

    buy_dates: dict[str, dict[str, str]] = {}

    price_map: dict[str, float] = {}
    prices = db.execute('SELECT * FROM product_prices').fetchall()
    for price_entry in prices:
        [product_id, price] = price_entry
        price_map[product_id] = price

    client_map: dict[str, float] = {}
    clients = db.execute('SELECT * FROM client_fees').fetchall()
    for client_entry in clients:
        [client_id, fee] = client_entry
        client_map[client_id] = fee

    result = []
    for order in orders:
        [_, client_id, product_id, type, quantity, timestamp] = order

        if client_id not in buy_dates:
            buy_dates[client_id] = {}

        price = price_map[product_id]

        if type == 'buy':
            buy_dates[client_id][product_id] = timestamp
        else:
            start_timestamp = buy_dates[client_id][product_id]
            difference = relativedelta(datetime.fromisoformat(timestamp), datetime.fromisoformat(start_timestamp))
            difference_in_months = difference.years * 12 + difference.months + 1


            fee_percent = (1 + (client_map[client_id] / 100) / 12) ** (12 * (difference_in_months / 12))
            price = round(price * fee_percent, 2)

        # Without this date aren't comparable because only one date has timezone offset
        order_date = datetime.fromisoformat(timestamp).replace(tzinfo=None)

        if from_date is not None and order_date < datetime.fromisoformat(from_date):
            continue

        result.append({
            "clientId": client_id,
            "productId": product_id,
            "orderType": type,
            "price": price,
            "quantity": quantity,
            "timestamp": timestamp
        })

    return result


def get_transactions_by_product(product_id, from_date=None, to_date=None):  # noqa: E501
    """get_transactions_by_product

    Time-series of transactions by product # noqa: E501

    :param product_id: Product Identifier
    :type product_id: str
    :param from_date: Include transactions starting and including date, default to today
    :type from_date: str
    :param to_date: Include transactions ending and including date, default to today
    :type to_date: str

    :rtype: List[Transaction]
    """
    db: Connection = request.state.db

    for date_value in [from_date, to_date]:
        if date_value is None:
            continue

        try:
            datetime.fromisoformat(date_value)
        except ValueError:
            return {'message': 'Bad date param - ' + date_value}, 400

    condition = ''
    if to_date is not None:
        condition += ' and date(timestamp) <= date(?)'

    remove_none_values = lambda l: [x for x in l if x is not None]

    orders = db.execute(
        f'SELECT * FROM orders WHERE productId = ? {condition} ORDER BY timestamp ASC',
        [product_id, *remove_none_values([to_date])])

    # Assuming that the client can buy only once!
    # But this is not mentioned in task description so calculating price is more complicated.

    buy_dates: dict[str, dict[str, str]] = {}

    price_map: dict[str, float] = {}
    prices = db.execute('SELECT * FROM product_prices').fetchall()
    for price_entry in prices:
        [product_id, price] = price_entry
        price_map[product_id] = price

    client_map: dict[str, float] = {}
    clients = db.execute('SELECT * FROM client_fees').fetchall()
    for client_entry in clients:
        [client_id, fee] = client_entry
        client_map[client_id] = fee

    result = []
    for order in orders:
        [_, client_id, product_id, type, quantity, timestamp] = order

        if client_id not in buy_dates:
            buy_dates[client_id] = {}

        price = price_map[product_id]

        if type == 'buy':
            buy_dates[client_id][product_id] = timestamp
        else:
            start_timestamp = buy_dates[client_id][product_id]
            difference = relativedelta(datetime.fromisoformat(timestamp), datetime.fromisoformat(start_timestamp))
            difference_in_months = difference.years * 12 + difference.months + 1

            fee_percent = (1 + (client_map[client_id] / 100) / 12) ** (12 * (difference_in_months / 12))
            price = round(price * fee_percent, 2)

        # Without this date aren't comparable because only one date has timezone offset
        order_date = datetime.fromisoformat(timestamp).replace(tzinfo=None)

        if from_date is not None and order_date < datetime.fromisoformat(from_date):
            continue

        result.append({
            "clientId": client_id,
            "productId": product_id,
            "orderType": type,
            "price": price,
            "quantity": quantity,
            "timestamp": timestamp
        })

    return result
