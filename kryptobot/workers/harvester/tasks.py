from .celery import app
from ..base_task import BaseTask
from ...portfolio.exchanges import Exchanges
from ...harvesters.arbitrage_harvester import ArbitrageHarvester


# TODO: Find a way to load configs for celery jobs
# Also api keys on this side multitenant
# config = getcwd() + '/config.json'
config = {
        "db": {
            "engine": "sqlite",
            "name": "core.db",
            "username": "",
            "password": "",
            "host": ""
        },
        "apis": {
            "cryptopia": {
                "key": "key",
                "secret": "secret"
            },
            "bittrex": {
                "key": "key",
                "secret": "secret"
            },
            "hitbtc": {
                "key": "key",
                "secret": "secret"
            },
            "binance": {
                "key": "key",
                "secret": "secret"
            }
        }
    }

exchanges = Exchanges(config['apis'])


# TODO: get this to work instead of depending on naming conventions and/or importing everything
# def import_harvester(class_name):
#     package = __import__('kryptobot')
#     print('package', dir(package))
#     harvesters = getattr(package, 'harvesters')
#     print('harvesters', dir(harvesters))
#     return getattr(harvesters, class_name)


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def import_harvester(harvester):
    harvester = to_camel_case(harvester)
    return globals()[harvester]


@app.task(base=BaseTask)
def launch_harvester(harvester, params):
    harvester = import_harvester(harvester)
    # bot = Bot(harvester(**params))
    # return bot.start()


@app.task(base=BaseTask)
def load_open_harvesters():
    return 'load_open_harvesters not implemented yet'
