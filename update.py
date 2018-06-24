# encoding: utf-8

from workflow import web, Workflow, PasswordNotFound


def get_recent_currencies_info():
    """ Retrieve recent currencies from http://coinmarketcap.com/
    Returns a list of currencies' information
    """

    # Get the information of the top 100 most popular currencies from the
    # website
    url = "https://api.coinmarketcap.com/v1/ticker/?start=0&limit=1000"
    r = web.get(url)

    # Throw an error if request failed
    # Workflow will catch this and show it to the user
    r.raise_for_status()

    # Parse the JSON returned by coinmarketcap.com
    result = r.json()
    return result


def main(wf):
    currencies = wf.cached_data(
        'currencies', get_recent_currencies_info, max_age=60)


if __name__ == '__main__':
    wf = Workflow()
    wf.run(main)
