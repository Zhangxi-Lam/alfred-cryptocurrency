from workflow import ICON_INFO
from config import COIN_ICON, APP_ICON
from workflow.background import run_in_background, is_running
from bitcoin_currency_exception import NoResultException
from collections import OrderedDict


def get_currency_title(currency):
    return currency['name']


def get_currency_subtitle(currency):
    postfix = OrderedDict([
        ('symbol', ""),
        ('price_usd', "$"),
        ('percent_change_1h', "%(1h)"),
        ('percent_change_24h', "%(24h)"),
        ('percent_change_7d', "%(7d)"),
    ])
    subtitle = []
    for key, value in postfix.iteritems():
        if currency[key]:
            subtitle.append(currency[key] + value)
    return u', '.join(subtitle)


def get_currency_icon(currency=None):
    return COIN_ICON


def get_app_icon():
    return APP_ICON


def search_key_for_currencies(currency):
    """Generate a string search key for a currecny"""
    elements = []
    elements.append(currency['id'])
    elements.append(currency['name'])
    elements.append(currency['symbol'])
    return u' '.join(elements)


def get_currencies_info(wf, query=None):
    # Create the currency for US dollar
    if query == "usd":
        currencies = []
        currencies.append({
            "symbol": "usd",
            "id": "usd",
            "name": "US Dollar",
            "price_usd": '1',
            "percent_change_1h": "",
            "percent_change_24h": "",
            "percent_change_7d": ""
        })
        return currencies
    # Get currencies info from cache. Set 'data_func' to None, as we don't want
    # to update the cache in this script and 'max_age' to 0 because we want
    # the cached data regardless of age
    currencies = wf.cached_data('currencies', None, max_age=0)

    # Start update script if cached data is too old (or doesn't exist)
    if not wf.cached_data_fresh('currencies', max_age=60):
        cmd = ['/usr/bin/python', wf.workflowfile('update.py')]
        run_in_background('update', cmd)

    if is_running('update'):
        wf.add_item(
            'Getting new currencies info from http://coinmarketcap.com/',
            valid=False,
            icon=ICON_INFO)

    # If script was passed a query, use it to filter currencies if we have some
    if query and currencies:
        currencies = wf.filter(
            query, currencies, key=search_key_for_currencies, min_score=90)
    return currencies


def show_basic_info(wf, query=None):
    # Get currencies info from cache. Set 'data_func' to None, as we don't want
    # to update the cache in this script and 'max_age' to 0 because we want
    # the cached data regardless of age
    currencies = get_currencies_info(wf, query)
    if not currencies:  # we have no data to show, so show a warning and stop
        raise NoResultException

    # Loop through the returned currencies and add a item for each to
    # the list of results for Alfred
    for currency in currencies:
        wf.add_item(
            title=get_currency_title(currency),
            subtitle=get_currency_subtitle(currency),
            arg=get_currency_title(currency),
            valid=True,
            icon=get_currency_icon(currency))

    wf.send_feedback()
    return 0


def show_help(wf, query=None):
    wf.add_item(
        title="bc Bitcoin",
        subtitle="Search the current status of Bitcoin.",
        icon=get_currency_icon())
    wf.add_item(
        title="bc Bitcoin 15",
        subtitle="Search how much are 15 Bitcoins in US dollars.",
        icon=get_currency_icon())
    wf.add_item(
        title="bc Bitcoin:Ethereum 2.5",
        subtitle="Search how much are 2.5 Bitcoins in Ethereum.",
        icon=get_currency_icon())
    wf.add_item(
        title="bcs",
        subtitle=
        "Search the top 10 Crytocurrency with largest increasement in the past 7 days.",
        icon=get_currency_icon())
    wf.add_item(
        title="bcs dec",
        subtitle=
        "Search the top 10 Crytocurrency with largest decline in the past 7 days.",
        icon=get_currency_icon())
    wf.add_item(
        title="bcs inc 5",
        subtitle=
        "Search the top 5 Crytocurrency with largest increasement in the past 7 days.",
        icon=get_currency_icon())
    wf.add_item(
        title="bcs inc 7 1h",
        subtitle=
        "Search the top 7 Crytocurrency with largest increasement in the past 1 hour.",
        icon=get_currency_icon())
    wf.add_item(
        title="bcs inc 3 24h",
        subtitle=
        "Search the top 3 Crytocurrency with largest increasement in the past 24 hours.",
        icon=get_currency_icon())
    wf.send_feedback()
    return 0
