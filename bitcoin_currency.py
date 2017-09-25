import sys
from workflow import Workflow, ICON_WARNING, ICON_ERROR, ICON_INFO
from basic_info import show_basic_info, show_help
from currency import show_currency
from bitcoin_currency_exception import InputFormatException, NoResultException

__version__ = '1.0'


def main(wf):
    # Get query from Alfred
    try:
        args = wf.args[0].split(' ')
        if len(args) == 1:
            if args[0] == "help":
                show_help(wf, args[0])
            else:
                show_basic_info(wf, args[0])
        elif len(args) <= 3:
            show_currency(wf, args)
        else:
            raise InputFormatException
    except NoResultException:
        return 0
    except InputFormatException:
        return 0


if __name__ == u"__main__":
    wf = Workflow(update_settings={
        'github_slug': 'zhangxi-Lam/alfred-cryptocurrency',
        'version': __version__,
        'frequency': 7,
    })
    sys.exit(wf.run(main))
