from .base import Base
from ..db.utils import get_or_create, sort_dict
from ..workers.t2.tasks import schedule_t2_strategy
from ..db.models import Strategy


class Params(dict):

    def update(self, *args):
        dict.update(self, *args)
        return self


class ParameterTester(Base):

    def __init__(self, batch_id, portfolio, strategy, exchange, pair, interval, params):
        super().__init__(batch_id, portfolio)
        self.strategy = strategy
        base, quote = pair.split('/')
        self.params = params
        self.strategy_params = Params({
            'type': 't2',
            'strategy': strategy,
            'limits': {
                'capital_base': 1000,
                'order_quantity': 100,
                'position_limit': 1000,
                'profit_target_percentage': 1.2,
                'fixed_stoploss_percentage': .95,
                'trailing_stoploss_percentage': .90
            },
            'default': {
                'interval': interval,
                'exchange': exchange,
                'base_currency': base,
                'quote_currency': quote,
                'is_simulated': True
            },
            'portfolio': {
                'name': self.portfolio.name
            }
        })

    def add_record(self, model, **kwargs):
        defaults = {
            'status': kwargs.pop('status', None)
        }
        return get_or_create(
            self._session,
            model,
            defaults,
            **kwargs
        )

    def schedule_strategy(self, custom_params):
        params = self.strategy_params.update({
            'custom': custom_params
        })
        params['portfolio_id'] = self.portfolio.id
        params = sort_dict(params)
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
        strategy.status = 'active'
        self._session.commit()
        schedule_t2_strategy.apply_async(
            None,
            {'params': params},
            task_id=strategy.celery_id
        )

    def run(self):
        pass
