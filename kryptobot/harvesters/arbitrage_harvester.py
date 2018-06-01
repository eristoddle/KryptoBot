from .base_harvester import BaseHarvester


class ArbitrageHarvester(BaseHarvester):

    def __init__(self, interval, is_simulated):
        super().__init__(interval, is_simulated)

    def on_data(self, data):
        pass
