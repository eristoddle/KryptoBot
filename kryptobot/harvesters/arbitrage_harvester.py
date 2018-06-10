from .base_harvester import BaseHarvester
from ..portfolio.exchanges import Exchanges


class ArbitrageHarvester(BaseHarvester):

    def __init__(self, interval, is_simulated, base_currency, threshold_percentage, portfolio_id, exchanges):
        kwargs = {
            'base_currency': base_currency,
            'threshold_percentage': threshold_percentage,
            'exchanges': exchanges
        }
        super().__init__(interval, is_simulated, portfolio_id, kwargs)
        self.taskname = 'arbitrage-harvester'
        self.classname = 'ArbitrageHarvester'
        self.base_currency = base_currency
        self.threshold_percentage = threshold_percentage
        self.exchanges = exchanges

    def get_data(self):
        apis = Exchanges(self.exchanges)
        prices = apis.get_arbitrage_prices(self.base_currency, self.threshold_percentage)
        return prices
