from .base_harvester import BaseHarvester
from ..portfolio.exchanges import Exchanges


class ArbitrageHarvester(BaseHarvester):

    taskname = 'arbitrage-harvester'
    classname = 'ArbitrageHarvester'

    def __init__(self, interval, is_simulated, base_currency, threshold_percentage, portfolio_id, harvester_id, config):
        kwargs = {
            'base_currency': base_currency,
            'threshold_percentage': threshold_percentage
        }
        super().__init__(interval, is_simulated, portfolio_id, harvester_id, config, kwargs)
        self.base_currency = base_currency
        self.threshold_percentage = threshold_percentage

    def get_data(self):
        exchanges = Exchanges(self.config['apis'])
        prices = exchanges.get_arbitrage_prices(self.base_currency, self.threshold_percentage)
        return prices
