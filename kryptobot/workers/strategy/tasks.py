from __future__ import absolute_import, unicode_literals
# import imp
from .celery import app
from ...bots.bot import Bot
from ...strategies.poc_strategy import PocStrategy


# TODO: get this to work instead of depending on naming conventions and/or importing everything
# def import_strategy(class_name):
#     package = __import__('kryptobot')
#     print('package', dir(package))
#     strategies = getattr(package, 'strategies')
#     print('strategies', dir(strategies))
#     return getattr(strategies, class_name)


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def import_strategy(strategy):
    strategy = to_camel_case(strategy)
    return globals()[strategy]


@app.task
def launch_strategy(strategy, params):
    strategy = import_strategy(strategy)
    bot = Bot(strategy(**params))
    return bot.start()


@app.task
def load_open_strategies():
    return 'load_open_strategies not implemented yet'
