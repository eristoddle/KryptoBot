from .base_harvester import BaseHarvester
from ..portfolio.exchanges import Exchanges


class ArbitrageHarvester(BaseHarvester):

    def __init__(self, interval, is_simulated):
        kwargs = {
            'harvester': 'ArbitrageHarvester'
        }
        super().__init__(interval, is_simulated, kwargs)
        self.taskname = 'arbitrage-harvester'

    def get_data(self):
        pass
