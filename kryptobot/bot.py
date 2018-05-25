from .publishers.ticker import Ticker
from .core import Core


class Bot(Core):

    strategy = None

    def __init__(self, strategy, config=None):
        super().__init__(config)
        self.strategy = strategy

    def __start(self):
        # TODO: All these adds are stupid, fix it
        self.strategy.add_session(self.session)
        self.strategy.add_keys(self.config['apis'])
        self.strategy.add_ticker(Ticker)
        self.strategy.run_simulation()
        self.strategy.start()

    def start(self):
        try:
            self.__start()

        except Exception as e:
            print(e)

        finally:
            self.engine.dispose()
