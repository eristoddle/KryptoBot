from .workers.strategy_worker import add, launch_strategy


class Hydra:

    def __init__(self):
        pass

    def launch_harvester(self):
        pass

    def launch_s(self):
        add.delay(4, 4)
        launch_strategy.delay('PocStrategy', '5m', 'bittrex', 'ETH/BTC', True)

    def test(self):
        self.launch_s()
