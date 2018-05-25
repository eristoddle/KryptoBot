from __future__ import absolute_import, unicode_literals
from .celery import app
from ...bot import Bot
from ...strategies.poc_strategy import PocStrategy


@app.task
def add(x, y):
    return x + y


@app.task
def launch_strategy(strategy, exchange, interval, pair, is_simulated):
    bot = Bot(PocStrategy("5m", 'bittrex', 'SYS', 'BTC', True, 12, 96, sim_balance=10))
    # bot.start()
    return bot.start()


@app.task
def load_open_strategies():
    return 'loaded open strategies'
    pass
