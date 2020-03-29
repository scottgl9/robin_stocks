"""Contains functions to get information about crypto-currencies."""
import robin_stocks.helper as helper
import robin_stocks.urls as urls


@helper.login_required
def load_crypto_profile(info=None):
    """Gets the information associated with the crypto account.

    :param info: The name of the key whose value is to be returned from the function.
    :type info: Optional[str]
    :returns: The function returns a dictionary of key/value pairs. \
    If a string is passed in to the info parameter, then the function will return \
    a string corresponding to the value of the key whose name matches the info parameter.

    """
    url = urls.crypto_account()
    data = helper.request_get(url, 'indexzero')
    return(helper.filter(data, info))


@helper.login_required
def get_crypto_positions(info=None):
    """Returns crypto positions for the account.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each option. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.crypto_holdings()
    data = helper.request_get(url, 'pagination')
    return(helper.filter(data, info))


def get_crypto_currency_pairs(info=None):
    """Gets a list of all the cypto currencies that you can trade

    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.

    """
    url = urls.crypto_currency_pairs()
    data = helper.request_get(url, 'results')
    return(helper.filter(data, info))


def get_crypto_info(symbol, info=None):
    """Gets information about a crpyto currency.

    :param symbol: The crypto ticker.
    :type symbol: str
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.

    """
    url = urls.crypto_currency_pairs()
    data = helper.request_get(url, 'results')
    data = [x for x in data if x['asset_currency']['code'] == symbol]
    if len(data) > 0:
        data = data[0]
    else:
        data = None
    return(helper.filter(data, info))


@helper.login_required
def get_crypto_quote(symbol, info=None):
    """Gets information about a crypto including low price, high price, and open price

    :param symbol: The crypto ticker.
    :type symbol: str
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.

    """
    id = get_crypto_info(symbol, info='id')
    url = urls.crypto_quote(id)
    data = helper.request_get(url)
    return(helper.filter(data, info))


@helper.login_required
def get_crypto_quote_from_id(id, info=None):
    """Gets information about a crypto including low price, high price, and open price. Uses the id instead of crypto ticker.

    :param id: The id of a crypto.
    :type id: str
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.

    """
    url = urls.crypto_quote(id)
    data = helper.request_get(url)
    return(helper.filter(data, info))


@helper.login_required
def get_crypto_historical(symbol, interval, span, bound, info=None):
    """Gets historical information about a crypto including open price, close price, high price, and low price.

    :param symbol: The crypto ticker.
    :type symbol: str
    :param interval: The time between data points.
    :type interval: str
    :param span: The entire time frame to collect data points.
    :type span: str
    :param bound: The times of dat to collect data points.
    :type bound: str
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.

    """
    interval_check = ['15second', '5minute', '10minute', 'hour', 'day', 'week']
    span_check = ['hour', 'day', 'week', 'month', '3month', 'year', '5year']
    bounds_check = ['24_7', 'extended', 'regular', 'trading']

    if interval not in interval_check:
        print(
            'ERROR: Interval must be "15second","5minute","10minute","hour","day",or "week"')
        return([None])
    if span not in span_check:
        print('ERROR: Span must be "hour","day","week","month","3month","year",or "5year"')
        return([None])
    if bound not in bounds_check:
        print('ERROR: Bounds must be "24_7","extended","regular",or "trading"')
        return([None])
    if (bound == 'extended' or bound == 'trading') and span != 'day':
        print('ERROR: extended and trading bounds can only be used with a span of "day"')
        return([None])

    id = get_crypto_info(symbol, info='id')
    url = urls.crypto_historical(id, interval, span, bound)
    data = helper.request_get(url)
    return(helper.filter(data, info))
