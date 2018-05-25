from __future__ import absolute_import, unicode_literals
from .celery import app


@app.task
def add(x, y):
    return x + y


@app.task
# PocStrategy("5m", 'bittrex', 'SYS', 'BTC', True, 12, 96, sim_balance=10)
def launch_strategy(strategy, exchange, interval, pair, is_simulated):
    # bot = Bot()
    print(strategy, exchange, interval, pair, is_simulated)
    return strategy
