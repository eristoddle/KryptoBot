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
#
# TODO: Redbeat jobs aren't encrypted and db creds are passed


class BaseHarvester:

    def __init__(self, interval, is_simulated, portfolio_id, harvester_id, config, kwargs):
        self.taskname = 'base-harvester'
        self.kwargs = kwargs
        self.harvester_id = harvester_id
        self.kwargs['harvester_id'] = harvester_id
        self.config = config
        self.kwargs['config'] = config
        self.interval = interval
        self.kwargs['interval'] = interval
        self.is_simulated = is_simulated
        self.kwargs['is_simulated'] = is_simulated
        self.portfolio_id = portfolio_id
        self.kwargs['portfolio_id'] = portfolio_id

    def create_schedule(self, app):
        data = {
            'classname': self.classname,
            'params': self.kwargs
        }
        interval = schedules.schedule(run_every=self.interval)
        entry = RedBeatSchedulerEntry(
            self.taskname,
            'kryptobot.workers.harvester.tasks.launch_harvester',
            interval,
            kwargs=data,
            app=app
        )
        entry.save()

    def get_data(self):
        return 'You should replace this in child classes'
