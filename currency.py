from bitcoin_currency_exception import InputFormatException
from basic_info import get_currencies_info


def show_currency(wf, args):
    if len(args) == 2:
        try:
            calculate_currency(wf, src=args[0], quantity=float(args[1]))
        except ValueError:
            calculate_currency(wf, src=args[0], dest=args[1])
    elif len(args) == 3:
        try:
            calculate_currency(
                wf, src=args[0], dest=args[1], quantity=float(args[2]))
        except ValueError:
            raise InputFormatException


def calculate_currency(wf, src, dest='usd', quantity=1):
    src_currencies = get_currencies_info(wf, src)
    dest_currencies = get_currencies_info(wf, dest)
    for sc in src_currencies:
        for dc in dest_currencies:
            if is_valid(sc) and is_valid(dc):
                wf.add_item(
                    title="{} -> {}".format(sc['name'], dc['name']),
                    subtitle="{} {} = {} {}".format(quantity, sc['name'],
                                                    calculate(
                                                        sc, dc, quantity),
                                                    dc['name']))
    wf.send_feedback()
    return 0


def calculate(src, dest, quantity):
    return float(src['price_usd']) * quantity / float(dest['price_usd'])


def is_valid(currency):
    return currency['symbol'] and currency['price_usd']
