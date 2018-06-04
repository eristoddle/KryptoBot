from ..core import Core
from ..db.models import Portfolio
from ..db.utils import get_or_create
from ..workers.strategy.tasks import launch_strategy, load_open_strategies
from ..workers.harvester.tasks import launch_harvester, load_open_harvesters
from .exchanges import Exchanges


class Manager(Core):

    exchanges = None
    portfolio_name = 'default'
    portfolio = None

    def __init__(self, config=None):
        super().__init__(config)
        if 'portfolio' in self.config and 'name' in self.config['portfolio']:
            self.portfolio_name = self.config['portfolio']['name']
            self.portfolio = get_or_create(self.session(), Portfolio, name='default')
        if 'apis' in self.config:
            self.exchanges = Exchanges(self.config['apis'])

    def run_harvester(self, harvester_name, params):
        params['porfolio_id'] = self.portfolio.id
        params['exchanges'] = self.exchanges
        launch_harvester.delay(harvester_name, params)

    def run_strategy(self, strategy_name, params):
        # params['porfolio_id'] = self.portfolio.id
        # params['exchanges'] = self.exchanges
        launch_strategy.delay(strategy_name, params)
