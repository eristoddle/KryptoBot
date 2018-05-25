from .workers.strategy.tasks import launch_strategy, load_open_strategies
from .workers.harvester.tasks import launch_harvester, load_open_harvesters

class Hydra:

    def __init__(self):
        load_open_strategies.delay()
        load_open_harvesters.delay()

    def run_harvester(self, harvester_name, params):
        launch_harvester.delay(harvester_name, params)

    def run_strategy(self, strategy_name, params):
        launch_strategy.delay(strategy_name, params)
