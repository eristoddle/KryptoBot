from rq import Connection, Worker
from ..bot import Bot


def launch_strategy():
    bot = Bot()


with Connection(host='redis', port=6379, db=0):
    worker = Worker('markets')
    worker.work()
