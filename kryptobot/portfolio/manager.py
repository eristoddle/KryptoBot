# from celery import uuid
import pandas as pd
import datetime
from ..core import Core
from ..db.models import Portfolio, Strategy, Harvester, Result, Backtest
from ..db.utils import get_or_create
from ..workers.strategy.tasks import schedule_strategy
from ..workers.harvester.tasks import schedule_harvester
from ..workers.catalyst.tasks import schedule_catalyst_strategy
from ..workers.core.tasks import schedule_core_strategy
from ..workers.t2.tasks import schedule_t2_strategy, stop_strategy


class Manager(Core):

    portfolio_name = 'default'
    portfolio = None

    def __init__(self, config=None):
        super().__init__(config)
        if 'portfolio' not in self.config:
            self.config['portfolio']['name'] = 'default'
        self._session = self.session()
        self.portfolio_name = self.config['portfolio']['name']
        self.portfolio = self.add_record(
            Portfolio,
            name=self.portfolio_name
        )

    def __del__(self):
        self._session.close()

    def add_record(self, model, **kwargs):
        return get_or_create(
            self._session,
            model,
            {},
            **kwargs
        )

    def run_harvester(self, params):
        if self.portfolio is not None:
            params['portfolio_id'] = self.portfolio.id
            harvester = self.add_record(
                Harvester,
                porfolio_id=self.portfolio.id,
                class_name=params['harvester'],
                params=params,
                status='active'
            )
            params['harvester_id'] = harvester.id
        params['config'] = self.config
        schedule_harvester.apply_async(
            None,
            {'params': params},
            task_id=harvester.celery_id
        )

    def run_strategy(self, params):
        if self.portfolio is not None:
            params['portfolio_id'] = self.portfolio.id
            strategy = self.add_record(
                Strategy,
                porfolio_id=self.portfolio.id,
                type=params['type'],
                class_name=params['strategy'],
                params=params,
                status='active'
            )
            params['strategy_id'] = strategy.id
        params['config'] = self.config
        if params['type'] == 'core':
            schedule_core_strategy.apply_async(
                None,
                {'params': params},
                task_id=strategy.celery_id
            )
        elif params['type'] == 'catalyst':
            schedule_catalyst_strategy.apply_async(
                None,
                {'params': params},
                task_id=strategy.celery_id
            )
        elif params['type'] == 't2':
            schedule_t2_strategy.apply_async(
                None,
                {'params': params},
                task_id=strategy.celery_id
            )
        else:
            schedule_strategy.apply_async(
                None,
                {'params': params},
                task_id=strategy.celery_id
            )

    def stop_strategy(self, celery_id):
        stop_strategy.delay(celery_id)

    def get_results(self, run_key, simulated=True):
        if simulated:
            Model = Backtest
        else:
            Model = Result
        results = self._session.query(Model).filter(Model.run_key == run_key).all()
        final = []
        for r in results:
            r.data['timestamp'] = self.convert_timestamp_to_date(r.data['timestamp'])
            final.append(r.data)
        return pd.DataFrame(final)

    def convert_timestamp_to_date(self, timestamp):
        value = datetime.datetime.fromtimestamp(float(str(timestamp)[:-3]))
        return value.strftime('%Y-%m-%d %H:%M:%S')
