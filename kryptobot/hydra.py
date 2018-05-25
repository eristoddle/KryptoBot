from rq import Queue
from redis import Redis
from .worker.strategy_worker import launch_strategy


class Hydra:

    def __init__(self):
        self.conn = Redis(host='redis', port=6379, db=0)

    def launch_harvester(self):
        pass

    def launch_strategy(self):
        q = Queue('strategies', connection=self.conn)
        q.enqueue(launch_strategy, 'http://nvie.com')
