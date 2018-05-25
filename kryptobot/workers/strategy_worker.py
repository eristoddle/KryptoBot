from rq import Connection, Worker
from redis import Redis
# from ..bot import Bot

conn = Redis(host='redis', port=6379, db=0)


# PocStrategy("5m", 'bittrex', 'SYS', 'BTC', True, 12, 96, sim_balance=10)
def launch_strategy(strategy, exchange, interval, pair, is_simulated):
    # bot = Bot()
    print(strategy, exchange, interval, pair, is_simulated)


with Connection(connection=conn):
    worker = Worker('strategies')
    worker.work()
