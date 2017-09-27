from bitcoin_currency_exception import InputFormatException
from basic_info import get_currencies_info, get_currency_icon


def show_currency(wf, src, dest, quanity=1):
    src_currencies = get_currencies_info(wf, src)
    dest_currencies = get_currencies_info(wf, dest)
    for sc in src_currencies:
        for dc in dest_currencies:
            if is_valid(sc) and is_valid(dc):
                wf.add_item(
                    title="{} -> {}".format(sc['name'], dc['name']),
                    subtitle="{} {} = {} {}".format(quanity, sc['name'],
                                                    calculate(sc, dc, quanity),
                                                    dc['name']),
                    icon=get_currency_icon(sc))
    wf.send_feedback()
    return 0


def calculate(src, dest, quanity):
    return float(src['price_usd']) * quanity / float(dest['price_usd'])


def is_valid(currency):
    return currency['symbol'] and currency['price_usd']
