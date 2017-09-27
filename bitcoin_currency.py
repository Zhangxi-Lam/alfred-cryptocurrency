import sys
from workflow import Workflow, ICON_INFO
from basic_info import show_basic_info, show_help
from currency import show_currency
from bitcoin_currency_exception import InputFormatException, NoResultException

SHOW_HELP = "Show help"
SHOW_BASIC_INFO = "Show basic info"
SHOW_CURRENCY = "Show currency"
ERROR = "Error"


def main(wf):
    # Get query from Alfred
    try:
        args = parse_params(wf.args[0])
        function = args["function"]
        if function == SHOW_HELP:
            show_help(wf)
        elif function == SHOW_BASIC_INFO:
            show_basic_info(wf, args["coin_1"])
        elif function == SHOW_CURRENCY:
            show_currency(wf, args["coin_1"], args["coin_2"], args["quanity"])
        else:
            raise InputFormatException
    except NoResultException:
        return 0
    except InputFormatException:
        return 0


def parse_params(args_str):
    args = {}
    args_params = args_str.split(':')
    if len(args_params) == 0:
        return args
    if len(args_params) == 1:
        args_params = args_params[0].split(' ')
        if len(args_params) == 1:
            if args_params[0] == "help":
                args["function"] = SHOW_HELP
                return args
            else:
                args["function"] = SHOW_BASIC_INFO
                args["coin_1"] = args_params[0]
                return args
        elif len(args_params) == 2:
            args["function"] = SHOW_CURRENCY
            args["coin_1"] = args_params[0]
            args["coin_2"] = "usd"
            try:
                args["quanity"] = float(args_params[1])
            except ValueError:
                args["function"] = ERROR
            return args
        else:
            args["function"] = ERROR
            return args
    elif len(args_params) == 2:
        args["function"] = SHOW_CURRENCY
        args["coin_1"] = args_params[0]
        try:
            args["quanity"] = float(args_params[1].split(' ')[-1])
            args["coin_2"] = ' '.join(args_params[1].split(' ')[:-1])
        except ValueError:
            args["coin_2"] = args_params[1]
            args["quanity"] = 1
        return args
    else:
        args["function"] = ERROR
        return args


wf = Workflow(update_settings={
    'github_slug': 'Zhangxi-Lam/alfred-cryptocurrency',
    'frequency': 7,
})

if wf.update_available:
    wf.add_item(
        'New version available',
        'Action this item to install the update',
        autocomplete='workflow:update',
        icon=ICON_INFO)
    wf.start_update()

sys.exit(wf.run(main))
