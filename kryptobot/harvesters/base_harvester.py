from celery import schedules
from redbeat import RedBeatSchedulerEntry
from ..db.models import Harvester, Portfolio


# TODO: Create scheduler class thats imported
# So you can choose celery or  pypubsub and queues


class BaseHarvester:

    def __init__(self, interval, is_simulated, portfolio_id=None):
        self.interval = interval
        self.is_simulated = is_simulated
        self.portfolio_id = portfolio_id
        self.create_record()

    def create_record(self):
        print('portfolio id', self.portfolio_id)

    def create_schedule(self):
        interval = schedules.schedule(run_every=60)
        entry = RedBeatSchedulerEntry('task-name', 'tasks.some_task', interval, args=['arg1', 2])
        entry.save()

    def on_data(self):
        return 'You should replace this in child classes'
