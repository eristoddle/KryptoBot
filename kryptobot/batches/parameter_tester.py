from .base import Base
from ..db.utils import get_or_create, sort_dict
from ..workers.t2.tasks import schedule_t2_strategy
from ..db.models import Strategy
import numpy as np


class Params(dict):

    def update(self, *args):
        dict.update(self, *args)
        return self


class ParameterTester(Base):

    def __init__(self, batch_id, portfolio_id, core, strategy, exchange, pair, interval, params):
        super().__init__(batch_id, portfolio_id, core)
        self.strategy = strategy
        base, quote = pair.split('/')
        self.params = params
        self.scheme = params.pop('scheme', None)
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
                'is_simulated': True,
                # 'backtest': True,
                # 'start': '2018-07-04',
                # 'end': '2018-07-11',
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
            batch_id=self.batch_id,
            type=params['type'],
            class_name=params['strategy'],
            params=params,
            status='active'
        )
        params['strategy_id'] = strategy.id
        params['config'] = self.config
        self._session.commit()
        schedule_t2_strategy.apply_async(
            None,
            {'params': params},
            task_id=strategy.celery_id
        )

    def generate_by_ratio(self):
        params_list = []
        start_params = {key: value[0] for (key, value) in self.params.items()}

        min_tuple = min(start_params.items(), key=lambda x: x[1])
        min_key = min_tuple[0]
        max_min = min_tuple[1]
        min_range = np.arange(self.params[min_key][1], max_min, self.scheme['step'])
        other_keys = [key[0] for (key) in self.params.items()]
        other_keys.remove(min_key)

        for min_val in min_range:
            new_params = {min_key: int(min_val)}
            for k in other_keys:
                if self.scheme['param_type'] == 'integer':
                    num = np.round((self.params[k][0] / max_min) * min_val)
                    new_params[k] = int(num)
                else:
                    new_params[k] = (self.params[k][0] / max_min) * min_val
            params_list.append(new_params)
        params_list.append(start_params)

        for p in params_list:
            self.schedule_strategy(p)


    def run(self):
        if 'relation' in self.scheme:
            if self.scheme['relation'] == 'ratio':
                self.generate_by_ratio()
