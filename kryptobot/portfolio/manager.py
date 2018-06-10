from ..core import Core
from ..db.models import Portfolio, Strategy, Harvester
from ..db.utils import get_or_create
from ..workers.strategy.tasks import schedule_strategy
from ..workers.harvester.tasks import schedule_harvester


class Manager(Core):

    portfolio_name = 'default'
    portfolio = None

    def __init__(self, config=None):
        super().__init__(config)
        if 'portfolio' in self.config and 'name' in self.config['portfolio']:
            self._session = self.session()
            self.portfolio_name = self.config['portfolio']['name']
            self.portfolio = get_or_create(
                self._session,
                Portfolio,
                name=self.portfolio_name
            )

    def __del__(self):
        self._session.close()

    def add_record(self, model):
        self._session.add(model)
        self._session.commit()

    def run_harvester(self, params):
        if self.portfolio is not None:
            params['portfolio_id'] = self.portfolio.id
        # TODO: Change this to use a config attribute like below
        params['exchanges'] = self.config['apis']
        if 'db' in self.config:
            params['db'] = self.config['db']
        schedule_harvester.delay(params)

    def run_strategy(self, params):
        if self.portfolio is not None:
            params['portfolio_id'] = self.portfolio.id
            strategy = Strategy(
                porfolio_id=self.portfolio.id,
                class_name=params['strategy'],
                params=params,
                status='active'
            )
        self.add_record(strategy)
        params['config'] = self.config
        schedule_strategy.delay(params)
