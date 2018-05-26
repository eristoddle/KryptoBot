from __future__ import absolute_import, unicode_literals
from .celery import app
from ...bots.bot import Bot
# from ...strategies.poc_strategy import PocStrategy


def import_strategy(class_name, module_name='kryptobot.strategies'):
    module = __import__(module_name)
    return getattr(module, class_name)


@app.task
def launch_strategy(strategy, params):
    strategy = import_strategy(strategy)
    print('########', strategy)
    return '#######'
    # bot = Bot(PocStrategy(**params))
    # return bot.start()


@app.task
def load_open_strategies():
    return 'load_open_strategies not implemented yet'
