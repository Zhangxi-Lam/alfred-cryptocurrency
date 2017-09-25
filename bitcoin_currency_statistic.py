import sys
from workflow import Workflow, ICON_WARNING, ICON_ERROR
from statistic import show_currency_statistic
from bitcoin_currency_exception import InputFormatException, NoResultException


def main(wf):
    # Get query from Alfred
    try:
        args = wf.args[0].split(' ')
        if len(args) == 1:
            if not args[0]:
                show_currency_statistic(wf)
            show_currency_statistic(wf, args[0])
        elif len(args) == 2:
            show_currency_statistic(wf, args[0], args[1])
        elif len(args) == 3:
            show_currency_statistic(wf, args[0], args[1], args[2])
        else:
            raise InputFormatException
    except NoResultException:
        #wf.add_item('No result found, please try again.', icon=ICON_WARNING)
        #wf.send_feedback()
        return 0
    except InputFormatException:
        #wf.add_item('Input format invald, please try again.', icon=ICON_ERROR)
        #wf.send_feedback()
        return 0


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
