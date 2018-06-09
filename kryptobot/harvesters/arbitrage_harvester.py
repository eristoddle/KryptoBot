from .base_harvester import BaseHarvester
from ..portfolio.exchanges import Exchanges


class ArbitrageHarvester(BaseHarvester):

    def __init__(self, interval, is_simulated, base_currency, threshold_percentage, portfolio_id, exchanges):
        print('ArbitrageHarvester')
        kwargs = {
            'base_currency': base_currency,
            'threshold_percentage': threshold_percentage,
            'exchanges': exchanges
        }
        super().__init__(interval, is_simulated, portfolio_id, kwargs)
        self.taskname = 'arbitrage-harvester'

    def get_data(self):
        print('ArbitrageHarvester get_data')
        return 'ArbitrageHarvester get_data'
