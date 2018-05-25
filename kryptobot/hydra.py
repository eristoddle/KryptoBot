from .workers.strategy.tasks import add, launch_strategy, load_open_strategies


class Hydra:

    def __init__(self):
        load_open_strategies()

    def launch_harvester(self):
        pass

    def launch_s(self):
        add.delay(4, 4)
        launch_strategy.delay('PocStrategy', '5m', 'bittrex', 'ETH/BTC', True)

    def test(self):
        self.launch_s()
