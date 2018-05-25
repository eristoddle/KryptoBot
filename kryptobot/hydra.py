from rq import Queue
from redis import Redis
from .workers.strategy_worker import launch_strategy


class Hydra:

    def __init__(self):
        self.conn = Redis(host='redis', port=6379, db=0)
        self.strategies_q = Queue('strategies', connection=self.conn)

    def launch_harvester(self):
        pass

    def launch_strategy(self):
        # PocStrategy("5m", 'bittrex', 'SYS', 'BTC', True, 12, 96, sim_balance=10)
        self.strategies_q.enqueue(launch_strategy, 'PocStrategy', '5m', 'bittrex', 'ETH/BTC', True)

    def test(self):
        self.launch_strategy()
        self.launch_strategy()
        self.launch_strategy()
        self.launch_strategy()
        self.launch_strategy()
