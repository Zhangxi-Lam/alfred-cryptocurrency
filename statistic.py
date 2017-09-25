from basic_info import get_currencies_info, get_currency_title, get_currency_subtitle, get_currency_icon
from bitcoin_currency_exception import InputFormatException
import heapq


def show_currency_statistic(wf, stat="inc", number=10, window="7d"):
    try:
        number = int(number)
    except ValueError:
        raise InputFormatException
    window = "percent_change_{}".format(window)
    currencies = get_currencies_info(wf)
    currencies = [
        currency for currency in currencies
        if window in currency.keys() and currency[window] != None
    ]

    if stat == "inc":
        result = heapq.nlargest(
            number, currencies, key=lambda e: float(e[window]))
    elif stat == "dec":
        result = heapq.nsmallest(
            number, currencies, key=lambda e: float(e[window]))
    else:
        raise InputFormatException

    for currency in result:
        wf.add_item(
            title=get_currency_title(currency),
            subtitle=get_currency_subtitle(currency),
            icon=get_currency_icon(currency))
    wf.send_feedback()

    return 0
