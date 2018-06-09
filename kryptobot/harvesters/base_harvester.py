from celery import schedules
from redbeat import RedBeatSchedulerEntry
from ..db.models import Harvester, Portfolio


# TODO: Create scheduler class thats imported
# So you can choose celery or pypubsub and queues
# Or make harvesters and strategies that are composites of Base Classes
# and queues
# Other dynamic scheduler option: https://github.com/liuliqiang/celerybeatredis
# Or: https://github.com/kongluoxing/celerybeatredis
#
# NOTE: Look into
# https://github.com/NetAngels/celery-tasktree


class BaseHarvester:

    def __init__(self, interval, is_simulated, portfolio_id, kwargs):
        self.taskname = 'base-harvester'
        self.kwargs = kwargs
        self.interval = interval
        self.kwargs['interval'] = interval
        self.is_simulated = is_simulated
        self.kwargs['is_simulated'] = is_simulated
        self.portfolio_id = portfolio_id
        self.kwargs['portfolio_id'] = portfolio_id
        # self.create_record()

    def create_record(self):
        print('portfolio id', self.portfolio_id)

    def create_schedule(self, app):
        interval = schedules.schedule(run_every=self.interval)
        entry = RedBeatSchedulerEntry(
            self.taskname,
            'kryptobot.workers.harvester.tasks.launch_harvester',
            interval,
            kwargs=self.kwargs,
            app=app
        )
        entry.save()

    def get_data(self):
        return 'You should replace this in child classes'
