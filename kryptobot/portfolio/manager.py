from ..core import Core
from ..db.models import Portfolio
from ..db.utils import get_or_create
from ..workers.strategy.tasks import schedule_strategy
from ..workers.harvester.tasks import schedule_harvester


class Manager(Core):

    exchanges = None
    portfolio_name = 'default'
    portfolio = None

    def __init__(self, config=None):
        super().__init__(config)
        if 'portfolio' in self.config and 'name' in self.config['portfolio']:
            self.portfolio_name = self.config['portfolio']['name']
            self.portfolio = get_or_create(self.session(), Portfolio, name='default')

    def run_harvester(self, params):
        params['portfolio_id'] = self.portfolio.id
        params['exchanges'] = self.config['apis']
        if 'db' in self.config:
            params['db'] = self.config['db']
        schedule_harvester.delay(params)

    def run_strategy(self, params):
        params['portfolio_id'] = self.portfolio.id
        params['exchanges'] = self.config['apis']
        if 'db' in self.config:
            params['db'] = self.config['db']
        schedule_strategy.delay(params)
