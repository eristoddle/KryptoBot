from __future__ import absolute_import, unicode_literals
from .celery import app
from ...bots.bot import Bot
from ...strategies.poc_strategy import PocStrategy


@app.task
def launch_strategy(strategy, params):
    bot = Bot(PocStrategy(**params))
    return bot.start()


@app.task
def load_open_strategies():
    return 'load_open_strategies not implemented yet'
